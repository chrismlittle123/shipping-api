import json
import os
from copy import copy
from pathlib import Path

import pytest

from src.data_ingestion.handler import (
    clean_column,
    clean_monitoring_methods,
    clean_null_values,
    clean_numerical_data,
    clean_raw_vessel_data,
    convert_csv_to_dictionaries,
    convert_date,
    create_vessel_item,
    extract_technical_efficiency,
    load_column_type_mappings,
)
from tests.resources.vessel_data import VESSEL_DATA_CLEAN, VESSEL_DATA_RAW

COLUMN_TYPE_MAPPINGS = load_column_type_mappings()


def test_clean_null_values():
    assert clean_null_values("") is None
    assert clean_null_values("n/a") is None
    assert clean_null_values("not applicable") is None
    assert clean_null_values("test") == "test"
    assert clean_null_values(5) == 5
    assert clean_null_values(5.3) == 5.3


def test_clean_column():
    assert clean_column("My Column%3Name") == "my_column_name"
    assert clean_column("Test  Column%5Name 1") == "test_column_name"
    assert clean_column("") == ""


def test_clean_numerical_data():
    assert clean_numerical_data(56) == 56.0
    assert clean_numerical_data("56.4") == 56.4
    assert clean_numerical_data("58") == 58.0
    assert clean_numerical_data("") is None
    assert clean_numerical_data("test") is None


def test_convert_date():
    assert convert_date("03/04/2020") == "2020-04-03"
    assert convert_date("6/7/2021") == "2021-07-06"
    assert convert_date("6-7-2021") is None


def test_clean_monitoring_methods():
    assert clean_monitoring_methods(None) == "No"
    assert clean_monitoring_methods("") == "No"
    assert clean_monitoring_methods("Yes") == "Yes"
    assert clean_monitoring_methods(" Yes") == "Yes"


def test_extract_technical_efficiency():
    assert extract_technical_efficiency("EIV (45.57 gCO₂/t·nm)") == 45.57
    assert extract_technical_efficiency("EIV (146 gCO₂/t·nm)") == 146.0
    assert extract_technical_efficiency("Not Applicable") is None
    assert extract_technical_efficiency("") is None
    assert extract_technical_efficiency("EIV") is None


def test_convert_csv_to_dictionaries():

    csv_content = [
        ["Column Name 1one", "Column%Name two2", "Column^Name three%3"],
        ["test1", "2", "3.0"],
        ["test4", "5.0", "six"],
    ]

    assert convert_csv_to_dictionaries(csv_content) == [
        {
            "column_name_one": "test1",
            "column_name_two": "2",
            "column_name_three": "3.0",
        },
        {
            "column_name_one": "test4",
            "column_name_two": "5.0",
            "column_name_three": "six",
        },
    ]


@pytest.mark.parametrize(
    "vessel_data_raw, vessel_data_clean",
    list(zip(copy(VESSEL_DATA_RAW), copy(VESSEL_DATA_CLEAN))),
)
def test_clean_raw_vessel_data(vessel_data_raw, vessel_data_clean):
    assert vessel_data_clean == clean_raw_vessel_data(
        vessel_data_raw, COLUMN_TYPE_MAPPINGS
    )


def test_create_vessel_item():

    vessel_data = copy(VESSEL_DATA_CLEAN)[0]

    json_path = os.path.join(
        *[Path(__file__).parents[1], "resources", "vessel_item.json"]
    )

    with open(json_path, "r") as file:
        vessel_item = json.load(file)

    assert create_vessel_item(vessel_data) == vessel_item
