import json

import requests
from aws_lambda_powertools.utilities.typing import LambdaContext


def create_vessel_item(raw_vessel_data: dict) -> dict:

    return {"a": 1, "b": 2}


def get_urls() -> dict:
    return {"cinch": "https://www.cinch.co.uk/"}


def handler(event: dict, context: LambdaContext) -> dict:
    urls = get_urls()
    sample_url = urls["cinch"]
    resp = requests.get(sample_url)
    return {
        "statusCode": resp.status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"response": resp.text}),
    }
