import json
import os
from copy import copy
from pathlib import Path

from src.data_ingestion.handler import (
    clean_raw_vessel_data,
    create_vessel_item,
    load_column_type_mappings,
    read_csv_from_s3,
)
from tests.resources.vessel_data import VESSEL_DATA_CLEAN, VESSEL_DATA_RAW


def test_clean_raw_vessel_data():

    column_type_mappings = load_column_type_mappings()
    vessel_data_raw = copy(VESSEL_DATA_RAW)
    vessel_data_clean = copy(VESSEL_DATA_CLEAN)

    assert vessel_data_clean == clean_raw_vessel_data(
        vessel_data_raw, column_type_mappings
    )


def test_read_csv_from_s3():
    event = {
        "Records": [
            {
                "eventVersion": "2.1",
                "eventSource": "aws:s3",
                "awsRegion": "us-west-2",
                "eventTime": "1970-01-01T00:00:00.000Z",
                "eventName": "ObjectCreated:Put",
                "userIdentity": {"principalId": "AIDAJDPLRKLG7UEXAMPLE"},
                "requestParameters": {"sourceIPAddress": "127.0.0.1"},
                "responseElements": {
                    "x-amz-request-id": "C3D13FE58DE4C810",
                    "x-amz-id-2": "FMyUVURIY8/IgAtTv8xRjskZQpcIZ9KG4V5Wp6S7S/JRWeUWerMUE5JgHvANOjpD",
                },
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "testConfigRule",
                    "bucket": {
                        "name": "shipping-api-495700631743",
                        "ownerIdentity": {"principalId": "A3NL1KOZZKExample"},
                        "arn": "arn:aws:s3:::shipping-api-495700631743",
                    },
                    "object": {
                        "key": "raw/year=2020/eu_mrv_shipping_data_2020.csv",
                        "size": 1024,
                        "eTag": "d41d8cd98f00b204e9800998ecf8427e",
                        "versionId": "096fKKXTRTtl3on89fVO.nfljtsv6qko",
                        "sequencer": "0055AED6DCD90281E5",
                    },
                },
            }
        ]
    }

    read_csv_from_s3(event)


def test_create_vessel_item():

    vessel_data = copy(VESSEL_DATA_CLEAN)

    json_path = os.path.join(
        *[Path(__file__).parents[1], "resources", "vessel_item.json"]
    )

    with open(json_path, "r") as file:
        vessel_item = json.load(file)

    assert create_vessel_item(vessel_data) == vessel_item
