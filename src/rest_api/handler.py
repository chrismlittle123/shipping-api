import json
import logging

from aws_lambda_powertools.utilities.typing import LambdaContext

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def handler(event: dict, context: LambdaContext) -> dict:

    LOGGER.info({"message": "Incoming API Gateway event", "content": json.dumps(event)})
    # 1. Parse out query string params
    transactionId = event["queryStringParameters"]["transactionId"]

    # 2. Construct the body of the response object
    transactionResponse = dict()
    transactionResponse["transactionId"] = transactionId
    transactionResponse["message"] = "Hello from Lambda land"

    # 3. Construct http response object
    responseObject = dict()
    responseObject["statusCode"] = "200"
    responseObject["headers"] = json.dumps({"Content-Type": "application/json"})
    responseObject["body"] = json.dumps(transactionResponse)

    # 4. Return the response object
    return responseObject
