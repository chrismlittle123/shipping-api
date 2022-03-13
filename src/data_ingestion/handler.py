import csv
import json
import logging
import urllib.parse
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
from src.models.pydantic_models import VesselItem
from src.models.pynamo_models import VesselItemModel

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
    vessel_item = VesselItemModel.write_vessel_item(item)
    if not vessel_item:
        LOGGER.warning(
            {
                "message": "Item could not be written to DynamoDB",
                "content": {
                    "item": item,
                },
            }
        )


def process_raw_vessel_data(
    vessel_data_raw: dict, column_type_mappings: dict
) -> Optional[dict]:
    """Process vessel data from raw form to clean nested and modelled dictionary

    Args:
        vessel_data_raw (dict): Raw vessel data as a flat dictionary
        column_type_mappings (dict): Mappings of column names to data types

    Returns:
        Optional[dict]: Cleaned, nested dictioniary with vessel data
    """
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


def get_vessel_generator(
    event: dict,
) -> Optional[Generator[Optional[dict], None, None]]:
    """Create a vessel generator which generates clean vessel items

    Args:
        event (dict): S3 event

    Returns:
        Optional[Generator[Optional[dict], None, None]]: Generator that
        yields clean vessel items
    """

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
