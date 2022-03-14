import json
import logging

from aws_lambda_powertools.utilities.typing import LambdaContext

from src.models.pynamo_models import VesselItemModel, VesselItemNotFound

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def handler(event: dict, context: LambdaContext) -> dict:

    LOGGER.info({"message": "Incoming API Gateway event", "content": json.dumps(event)})

    try:
        reporting_period = str(event["query"].get("reporting_period", ""))
        imo_number = event["query"].get("imo_number", "")

        vessel_item = VesselItemModel.read_vessel_item(reporting_period, imo_number)

        response = {
            "status_code": 200,
            "headers": {"content-type": "application/json"},
            "body": vessel_item,
        }
    except VesselItemNotFound:
        response = {"status_code": 404}

    return response
