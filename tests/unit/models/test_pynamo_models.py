from copy import deepcopy

from freezegun import freeze_time

from src.models.pynamo_models import VesselItemModel
from tests.resources.vessel_data import VESSEL_ITEMS


@freeze_time("2021-07-30T09:00:00Z")
def test_write_vessel_item(
    sample_vessel_item,
    shipping_data_table,
    aws_credentials,
):

    if not VesselItemModel.exists():
        VesselItemModel.create_table(
            read_capacity_units=123, write_capacity_units=123, wait=True
        )

    vessel_item = deepcopy(VESSEL_ITEMS[0])
    returned_item = VesselItemModel.write_vessel_item(vessel_item)
    assert returned_item == sample_vessel_item


@freeze_time("2021-07-30T09:00:00Z")
def test_read_vessel_item(sample_vessel_item, shipping_data_table, aws_credentials):

    if not VesselItemModel.exists():
        VesselItemModel.create_table(
            read_capacity_units=123, write_capacity_units=123, wait=True
        )

    vessel_item = deepcopy(VESSEL_ITEMS[0])
    VesselItemModel.write_vessel_item(vessel_item)

    reporting_period = 2018
    imo_number = "5383304"

    read_item = VesselItemModel.read_vessel_item(
        reporting_period=reporting_period, imo_number=imo_number
    )
    read_item["pk"] = "EU_MRV_EMISSIONS_DATA"
    read_item["sk"] = f"REPORTING_PERIOD#{reporting_period}#IMO_NUMBER#{imo_number}"
    read_item["updated_date"] = "2021-07-30 09:00:00"

    assert read_item == sample_vessel_item
