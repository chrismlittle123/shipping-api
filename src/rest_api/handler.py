import json
import logging
from typing import Any, Dict

from aws_lambda_powertools.utilities.typing import LambdaContext

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def handler(event: dict, context: LambdaContext) -> dict:

    LOGGER.info({"message": "Incoming API Gateway event", "content": json.dumps(event)})
    # 1. Parse out query string params
    transactionId = event["query"]["transactionId"]

    # 2. Construct the body of the response object

    response_1 = {"transactionId": transactionId, "message": "message 1"}
    response_2 = {"transactionId": transactionId, "message": "message 2"}

    # 3. Construct http response object
    responseObject: Dict[str, Any] = dict()
    responseObject["status_code"] = 200
    responseObject["headers"] = {"content-type": "application/json"}
    responseObject["body"] = [response_1, response_2]

    # 4. Return the response object
    return responseObject
