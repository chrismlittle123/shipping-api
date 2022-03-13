import json
import logging
from typing import Any, Dict

from aws_lambda_powertools.utilities.typing import LambdaContext

from src.models.pynamo_models import VesselItemModel

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def handler(event: dict, context: LambdaContext) -> dict:

    LOGGER.info({"message": "Incoming API Gateway event", "content": json.dumps(event)})

    reporting_period = event["query"]["reporting_period"]
    imo_number = event["query"]["imo_number"]

    vessel_item = VesselItemModel.read_vessel_item(reporting_period, imo_number)

    responseObject: Dict[str, Any] = dict()
    responseObject["status_code"] = 200
    responseObject["headers"] = {"content-type": "application/json"}
    responseObject["body"] = vessel_item

    return responseObject
