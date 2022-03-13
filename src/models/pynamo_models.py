import json
import os
from datetime import datetime
from typing import List, Union

from pynamodb.attributes import MapAttribute, NumberAttribute, UnicodeAttribute
from pynamodb.exceptions import PutError
from pynamodb.models import Model

from src.models.pydantic_models import VesselItem


class ShippingData(Model):
    class Meta:
        table_name = "shipping-data"
        region = os.environ["AWS_REGION"]

    pk = UnicodeAttribute(hash_key=True, attr_name="PK")
    sk = UnicodeAttribute(range_key=True, attr_name="SK")

    updated_date = UnicodeAttribute()

    imo_number = UnicodeAttribute()
    name = UnicodeAttribute()
    ship_type = UnicodeAttribute()
    reporting_period = NumberAttribute()
    technical_efficiency = NumberAttribute(null=True)
    port_of_registry = UnicodeAttribute(null=True)
    home_port = UnicodeAttribute(null=True)
    ice_class = UnicodeAttribute(null=True)
    doc_issue_date = UnicodeAttribute(null=True)
    doc_expiry_date = UnicodeAttribute(null=True)
    verifier_details: MapAttribute = MapAttribute()
    monitoring_methods: MapAttribute = MapAttribute()
    fuel_consumption_metrics: MapAttribute = MapAttribute()
    co2_emissions_metrics: MapAttribute = MapAttribute()
    time_metrics: MapAttribute = MapAttribute()
    distance_metrics: MapAttribute = MapAttribute()
    density_metrics: MapAttribute = MapAttribute()
    additional_information = UnicodeAttribute(null=True)


class VesselItemModel(ShippingData):
    def convert_to_dictionary(self) -> dict:

        model_dictionary = self.attribute_values
        for key, value in model_dictionary.items():
            if isinstance(value, MapAttribute):
                model_dictionary[key] = value.attribute_values

        return model_dictionary

    @classmethod
    def read_vessel_item(
        cls, reporting_period: str, imo_number: str
    ) -> Union[List[dict], None]:
        try:
            pk = "EU_MRV_EMISSIONS_DATA"
            sk = f"REPORTING_PERIOD#{reporting_period}#IMO_NUMBER#{imo_number}"

            vessel_item = list(VesselItemModel.query(pk, VesselItemModel.sk == sk))[0]

            vessel_item_pydantic_model = VesselItem(
                **vessel_item.convert_to_dictionary()
            )

            return json.loads(vessel_item_pydantic_model.json())
        except IndexError:
            return None

    @classmethod
    def write_vessel_item(cls, item: dict) -> Union[dict, None]:
        try:
            obj = cls(
                pk="EU_MRV_EMISSIONS_DATA",
                sk=f"REPORTING_PERIOD#{item['reporting_period']}#IMO_NUMBER#{item['imo_number']}",
                updated_date=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                **item,
            )
            obj.save()

            return obj.convert_to_dictionary()
        except PutError:
            return None
