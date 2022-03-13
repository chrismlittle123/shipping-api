from copy import deepcopy
from datetime import date

import pytest
from pydantic import ValidationError

from src.pydantic_models import Boolean, Unit, VesselItem
from tests.resources.vessel_data import VESSEL_ITEMS


def test_vessel_item_unhappy_path():
    vessel_item = deepcopy(VESSEL_ITEMS[0])
    vessel_item["imo_number"] = "12345678"
    with pytest.raises(ValidationError):
        VesselItem(**vessel_item)


def test_vessel_item_happy_path():
    vessel_item = deepcopy(VESSEL_ITEMS[0])
    vessel_item_object = VesselItem(**vessel_item)
    assert vessel_item_object.dict() == {
        "imo_number": "5383304",
        "name": "ASTORIA",
        "ship_type": "Passenger ship",
        "reporting_period": 2018,
        "technical_efficiency": None,
        "port_of_registry": None,
        "home_port": None,
        "ice_class": None,
        "doc_issue_date": date(2019, 2, 5),
        "doc_expiry_date": date(2020, 6, 30),
        "verifier_details": {
            "verifier_number": None,
            "verifier_name": "ICS VERIFICATION SERVICES SINGLE MEMBER P.C.",
            "verifier_accreditation_body": "HELLENIC ACCREDITATION SYSTEM (ESYD)",
            "verifier_address": "55 FILONOS STR.\n185 35 PIRAEUS, GREECE",
            "verifier_city": "PIRAEUS",
            "verifier_accreditation_number": "1101",
            "verifier_country": "GREECE",
        },
        "monitoring_methods": {
            "a": {
                "value": Boolean.yes,
                "description": "BDN and period stock takes of fuel tanks",
            },
            "b": {
                "value": Boolean.no,
                "description": "Bunker fuel tank monitoring on-board",
            },
            "c": {
                "value": Boolean.no,
                "description": "Flow meters for applicable combustion processes",
            },
            "d": {
                "value": Boolean.no,
                "description": "Direct CO2 emissions measurement",
            },
        },
        "fuel_consumption_metrics": {
            "all_voyages": {
                "total": {"value": 6307.75, "unit": Unit.metric_tonne},
                "annual_average": {
                    "per_distance": {"value": 139.07, "unit": Unit.emissions_distance},
                    "per_transport_work": {
                        "mass": {"value": None, "unit": Unit.emissions_mass},
                        "volume": {"value": None, "unit": Unit.emissions_volume},
                        "deadweight_tonnage": {
                            "value": None,
                            "unit": Unit.emissions_mass,
                        },
                        "passengers": {"value": 311.97, "unit": Unit.emissions_mass},
                        "freight": {"value": None, "unit": Unit.emissions_mass},
                    },
                },
            },
            "laden_voyages": {
                "total": {"value": None, "unit": Unit.metric_tonne},
                "per_distance": {"value": None, "unit": Unit.emissions_distance},
                "per_transport_work": {
                    "mass": {"value": None, "unit": Unit.emissions_mass},
                    "volume": {"value": None, "unit": Unit.emissions_volume},
                    "deadweight_tonnage": {"value": None, "unit": Unit.emissions_mass},
                    "passengers": {"value": None, "unit": Unit.emissions_mass},
                    "freight": {"value": None, "unit": Unit.emissions_mass},
                },
            },
        },
        "co2_emissions_metrics": {
            "all_voyages": {
                "total": {"value": 20080.25, "unit": Unit.metric_tonne},
                "between_ports": {
                    "value": 16035.42,
                    "unit": Unit.metric_tonne,
                    "description": "CO2 emissions from all voyages between ports under a Member State jurisdiction",
                },
                "departed_from_ports": {
                    "value": 728.59,
                    "unit": Unit.metric_tonne,
                    "description": "CO2 emissions from all voyages which departed from ports under a Member State jurisdiction",
                },
                "to_ports": {
                    "value": 974.78,
                    "unit": Unit.metric_tonne,
                    "description": "CO2 emissions from all voyages to ports under a Member State jurisdiction",
                },
                "within_ports_at_berth": {
                    "value": 2341.47,
                    "unit": Unit.metric_tonne,
                    "description": "CO2 emissions which occurred within ports under a Member State jurisdiction at berth",
                },
                "passenger_transport": {"value": None, "unit": Unit.metric_tonne},
                "freight_transport": {"value": None, "unit": Unit.metric_tonne},
                "annual_average": {
                    "per_distance": {"value": 442.71, "unit": Unit.emissions_distance},
                    "per_transport_work": {
                        "mass": {"value": None, "unit": Unit.emissions_mass},
                        "volume": {"value": None, "unit": Unit.emissions_volume},
                        "deadweight_tonnage": {
                            "value": None,
                            "unit": Unit.emissions_mass,
                        },
                        "passengers": {"value": 993.14, "unit": Unit.emissions_mass},
                        "freight": {"value": None, "unit": Unit.emissions_mass},
                    },
                },
            },
            "laden_voyages": {
                "total": {"value": None, "unit": Unit.metric_tonne},
                "per_distance": {"value": None, "unit": Unit.emissions_distance},
                "per_transport_work": {
                    "mass": {"value": None, "unit": Unit.emissions_mass},
                    "volume": {"value": None, "unit": Unit.emissions_volume},
                    "deadweight_tonnage": {"value": None, "unit": Unit.emissions_mass},
                    "passengers": {"value": None, "unit": Unit.emissions_mass},
                    "freight": {"value": None, "unit": Unit.emissions_mass},
                },
            },
        },
        "time_metrics": {
            "annual_total_time_spent_at_sea": {"value": 4170.2, "unit": Unit.hour},
            "total_time_spent_at_sea": {"value": 4170.2, "unit": Unit.hour},
            "total_time_spent_at_sea_through_ice": {"value": None, "unit": Unit.hour},
        },
        "distance_metrics": {
            "distance_travelled_through_ice": {
                "value": None,
                "unit": Unit.nautical_mile,
            }
        },
        "density_metrics": {
            "average_cargo_density": {"value": None, "unit": Unit.density}
        },
        "additional_information": None,
    }
