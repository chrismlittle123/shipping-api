from copy import deepcopy

import pytest

from src.data_ingestion.data_processing import load_column_type_mappings
from src.data_ingestion.handler import get_vessel_generator, process_raw_vessel_data
from tests.resources.vessel_data import VESSEL_DATA_RAW, VESSEL_ITEMS

COLUMN_TYPE_MAPPINGS = load_column_type_mappings()


@pytest.mark.parametrize(
    "vessel_data_raw, vessel_items",
    list(zip(deepcopy(VESSEL_DATA_RAW), deepcopy(VESSEL_ITEMS))),
)
def test_process_raw_vessel_data_happy_path(vessel_data_raw, vessel_items):

    assert vessel_items == process_raw_vessel_data(
        vessel_data_raw, COLUMN_TYPE_MAPPINGS
    )


def test_process_raw_vessel_data_validation_error(caplog):

    vessel_data_raw = deepcopy(VESSEL_DATA_RAW[0])
    vessel_data_raw["imo_number"] = "12345678"

    assert process_raw_vessel_data(vessel_data_raw, COLUMN_TYPE_MAPPINGS) is None

    logger_message = caplog.records[0].message
    expected_message = (
        "{'message': 'Vessel data could not be processed for reporting period: 2018 and IMO number: 12345678', "
        "'content': ValidationError(model='VesselItem', errors=[{'loc': ('imo_number',), "
        "'msg': 'IMO Number must be 7 digits long', 'type': 'value_error'}])}"
    )

    assert logger_message == expected_message


def test_process_raw_vessel_data_key_error(caplog):

    vessel_data_raw = deepcopy(VESSEL_DATA_RAW[0])
    del vessel_data_raw["imo_number"]

    assert process_raw_vessel_data(vessel_data_raw, COLUMN_TYPE_MAPPINGS) is None

    logger_message = caplog.records[0].message
    expected_message = "{'message': 'Vessel data did not include reporting period or IMO number', 'content': KeyError('imo_number')}"

    assert logger_message == expected_message


def test_get_vessel_generator(read_csv_from_s3):

    event = {"test-event-key": "test-event-value"}

    vessel_items = deepcopy(VESSEL_ITEMS[:5])
    expected_generator = (vessel_item for vessel_item in vessel_items)

    assert [item for item in get_vessel_generator(event)] == [
        item for item in expected_generator
    ]


def test_get_vessel_generator_unhappy_path(mocker):

    event = {"test-event-key": "test-event-value"}
    mocker.patch("src.data_ingestion.handler.read_csv_from_s3", return_value=None)

    assert get_vessel_generator(event) is None
