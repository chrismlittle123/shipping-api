import json
import requests


def get_urls() -> dict:
    return {"cinch": "https://www.cinch.co.uk/"}


def handler(event, context):
    urls = get_urls()
    sample_url = urls["cinch"]
    resp = requests.get(sample_url)
    return {
        "statusCode": resp.status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"response": resp.text}),
    }
