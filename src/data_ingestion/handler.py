import csv
import json
import logging
import urllib.parse
from datetime import datetime
from decimal import Decimal
from typing import Generator, List, Optional, Union

import boto3
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from src.data_ingestion.data_processing import (
    clean_raw_vessel_data,
    convert_csv_to_dictionaries,
    create_vessel_item,
    load_column_type_mappings,
)
from src.data_ingestion.pydantic_models import VesselItem

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def read_csv_from_s3(event: dict) -> Union[List[list], None]:

    s3_client = boto3.client("s3")

    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        content = response["Body"].read().decode("utf-8").splitlines(True)
        csv_reader = csv.reader(content, delimiter=",")
        return [row for row in csv_reader]
    except Exception as error:
        LOGGER.error(
            {"message": "Error when reading CSV file from S3", "content": error}
        )
        return None


def write_item_to_dynamodb(item: dict) -> None:

    if item:
        item = json.loads(json.dumps(item), parse_float=Decimal)

        item["PK"] = "EU_MRV_EMISSIONS_DATA"
        item[
            "SK"
        ] = f"REPORTING_PERIOD#{item['reporting_period']}#IMO_NUMBER#{item['imo_number']}"
        item["updated_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        dynamodb_table = "shipping-data"

        dynamodb = boto3.resource("dynamodb")

        table = dynamodb.Table(dynamodb_table)
        response = table.put_item(Item=item)

        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            LOGGER.warning(
                {
                    "message": "Item could not be written to DynamoDB",
                    "content": {
                        "status_code": response["ResponseMetadata"]["HTTPStatusCode"],
                        "item": item,
                    },
                }
            )


def process_raw_vessel_data(
    vessel_data_raw: dict, column_type_mappings: dict
) -> Optional[dict]:
    try:
        reporting_period = vessel_data_raw["reporting_period"]
        imo_number = vessel_data_raw["imo_number"]
        try:
            vessel_data = clean_raw_vessel_data(vessel_data_raw, column_type_mappings)
            vessel_item = create_vessel_item(vessel_data)
            vessel_item_object = VesselItem(**vessel_item)
            return json.loads(vessel_item_object.json())
        except ValidationError as error:
            LOGGER.warning(
                {
                    "message": f"Vessel data could not be processed for reporting period: {reporting_period} and IMO number: {imo_number}",
                    "content": error,
                }
            )
            return None
    except KeyError as error:
        LOGGER.warning(
            {
                "message": "Vessel data did not include reporting period or IMO number",
                "content": error,
            }
        )
        return None


# TO DO: Create API endpoints - get all data, get data based on year, get data based on imo number, get data based on name
# TO DO: Write tests for writing to DynamoDB - ie. integration tests for write_item_to_dynamodb and read_csv_from_s3 functions
# TO DO: Write end to end test - For example, one where I remove items from dynamoDB with certain IMO Numbers ("0000001", "0000002", "0000003", etc.)
# then I upload a CSV file to a S3 file location called "raw/e2e", then wait for 5 seconds, then I make graphQL query requests for each one of these
# vessels and check that the data matches.
# TO DO: Add docstrings to classes and functions where appropriate
# TO DO: Use sphinx to generate documentation for the Lambda
# TO DO: Add explanation of project including documentation for DynamoDB table in a separated Markdown file inside a docs folder. Put images of diagrams in data folder.
# TO DO: Get serverless deploy to work in GitHub Actions
# TO DO: Remember to send zip folder with code to Ahmad by Sunday evening
# TO DO: Think about table versioning or backups
# TO DO: Think about monitoring this API - how do I track metrics and ensure it's not breaking?


def get_vessel_generator(
    event: dict,
) -> Optional[Generator[Optional[dict], None, None]]:

    csv_content = read_csv_from_s3(event)
    column_type_mappings = load_column_type_mappings()

    if csv_content:
        vessel_data_raw_dictionaries = convert_csv_to_dictionaries(csv_content)
        vessel_generator = (
            process_raw_vessel_data(vessel_data_raw, column_type_mappings)
            for vessel_data_raw in vessel_data_raw_dictionaries
        )

        return vessel_generator
    return None


def handler(event: dict, context: LambdaContext) -> dict:
    LOGGER.info({"message": "Incoming S3 event", "content": json.dumps(event)})

    vessel_generator = get_vessel_generator(event)
    if vessel_generator:
        for vessel_item in vessel_generator:
            if vessel_item:
                write_item_to_dynamodb(vessel_item)

        return {"body": "Success!"}
    return {"body": "Unsuccesful"}
