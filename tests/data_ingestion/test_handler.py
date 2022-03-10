import json
import os
from copy import copy
from pathlib import Path

from src.data_ingestion.handler import (
    clean_raw_vessel_data,
    create_vessel_item,
    load_column_type_mappings,
)
from tests.resources.vessel_data import VESSEL_DATA_CLEAN, VESSEL_DATA_RAW


def test_clean_raw_vessel_data():

    column_type_mappings = load_column_type_mappings()
    vessel_data_raw = copy(VESSEL_DATA_RAW)
    vessel_data_clean = copy(VESSEL_DATA_CLEAN)

    assert vessel_data_clean == clean_raw_vessel_data(
        vessel_data_raw, column_type_mappings
    )


def test_create_vessel_item():

    vessel_data = copy(VESSEL_DATA_CLEAN)

    json_path = os.path.join(
        *[Path(__file__).parents[1], "resources", "vessel_item.json"]
    )

    with open(json_path, "r") as file:
        vessel_item = json.load(file)

    assert create_vessel_item(vessel_data) == vessel_item
