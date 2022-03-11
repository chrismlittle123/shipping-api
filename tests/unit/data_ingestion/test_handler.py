from copy import deepcopy

import pytest

from src.data_ingestion.data_processing import load_column_type_mappings
from src.data_ingestion.handler import process_raw_vessel_data
from tests.resources.vessel_data import VESSEL_DATA_RAW, VESSEL_ITEMS

COLUMN_TYPE_MAPPINGS = load_column_type_mappings()


@pytest.mark.parametrize(
    "vessel_data_raw, vessel_items",
    list(zip(deepcopy(VESSEL_DATA_RAW), deepcopy(VESSEL_ITEMS))),
)
def test_process_raw_vessel_data(vessel_data_raw, vessel_items):

    assert vessel_items == process_raw_vessel_data(
        vessel_data_raw, COLUMN_TYPE_MAPPINGS
    )
