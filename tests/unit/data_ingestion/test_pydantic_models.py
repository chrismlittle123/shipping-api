from copy import copy
from datetime import date

from src.data_ingestion.pydantic_models import Boolean, Unit, VesselItem
from tests.resources.vessel_data import VESSEL_ITEMS


def test_vessel_item():
    vessel_item = copy(VESSEL_ITEMS)[0]
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
                "total": {
                    "amount": None,
                    "unit": Unit.metric_tonne,
                    "description": None,
                },
                "annual_average": {
                    "per_distance": {
                        "amount": None,
                        "unit": Unit.emissions_distance,
                        "description": None,
                    },
                    "per_transport_work": {
                        "mass": {
                            "amount": None,
                            "unit": Unit.emissions_mass,
                            "description": None,
                        },
                        "volume": {
                            "amount": None,
                            "unit": Unit.emissions_volume,
                            "description": None,
                        },
                        "deadweight_tonnage": {
                            "amount": None,
                            "unit": Unit.emissions_mass,
                            "description": None,
                        },
                        "passengers": {
                            "amount": None,
                            "unit": Unit.emissions_mass,
                            "description": None,
                        },
                        "freight": {
                            "amount": None,
                            "unit": Unit.emissions_mass,
                            "description": None,
                        },
                    },
                },
            },
            "laden_voyages": {
                "total": {
                    "amount": None,
                    "unit": Unit.metric_tonne,
                    "description": None,
                },
                "per_distance": {
                    "amount": None,
                    "unit": Unit.emissions_distance,
                    "description": None,
                },
                "per_transport_work": {
                    "mass": {
                        "amount": None,
                        "unit": Unit.emissions_mass,
                        "description": None,
                    },
                    "volume": {
                        "amount": None,
                        "unit": Unit.emissions_volume,
                        "description": None,
                    },
                    "deadweight_tonnage": {
                        "amount": None,
                        "unit": Unit.emissions_mass,
                        "description": None,
                    },
                    "passengers": {
                        "amount": None,
                        "unit": Unit.emissions_mass,
                        "description": None,
                    },
                    "freight": {
                        "amount": None,
                        "unit": Unit.emissions_mass,
                        "description": None,
                    },
                },
            },
        },
        "co2_emissions_metrics": {
            "all_voyages": {
                "total": {
                    "amount": None,
                    "unit": Unit.metric_tonne,
                    "description": None,
                },
                "between_ports": {
                    "amount": None,
                    "unit": Unit.metric_tonne,
                    "description": "CO2 emissions from all voyages between ports under a Member State jurisdiction",
                },
                "departed_from_ports": {
                    "amount": None,
                    "unit": Unit.metric_tonne,
                    "description": "CO2 emissions from all voyages which departed from ports under a Member State jurisdiction",
                },
                "to_ports": {
                    "amount": None,
                    "unit": Unit.metric_tonne,
                    "description": "CO2 emissions from all voyages to ports under a Member State jurisdiction",
                },
                "within_ports_at_berth": {
                    "amount": None,
                    "unit": Unit.metric_tonne,
                    "description": "CO2 emissions which occurred within ports under a Member State jurisdiction at berth",
                },
                "passenger_transport": {
                    "amount": None,
                    "unit": Unit.metric_tonne,
                    "description": None,
                },
                "freight_transport": {
                    "amount": None,
                    "unit": Unit.metric_tonne,
                    "description": None,
                },
                "annual_average": {
                    "per_distance": {
                        "amount": None,
                        "unit": Unit.emissions_distance,
                        "description": None,
                    },
                    "per_transport_work": {
                        "mass": {
                            "amount": None,
                            "unit": Unit.emissions_mass,
                            "description": None,
                        },
                        "volume": {
                            "amount": None,
                            "unit": Unit.emissions_volume,
                            "description": None,
                        },
                        "deadweight_tonnage": {
                            "amount": None,
                            "unit": Unit.emissions_mass,
                            "description": None,
                        },
                        "passengers": {
                            "amount": None,
                            "unit": Unit.emissions_mass,
                            "description": None,
                        },
                        "freight": {
                            "amount": None,
                            "unit": Unit.emissions_mass,
                            "description": None,
                        },
                    },
                },
            },
            "laden_voyages": {
                "total": {
                    "amount": None,
                    "unit": Unit.metric_tonne,
                    "description": None,
                },
                "per_distance": {
                    "amount": None,
                    "unit": Unit.emissions_distance,
                    "description": None,
                },
                "per_transport_work": {
                    "mass": {
                        "amount": None,
                        "unit": Unit.emissions_mass,
                        "description": None,
                    },
                    "volume": {
                        "amount": None,
                        "unit": Unit.emissions_volume,
                        "description": None,
                    },
                    "deadweight_tonnage": {
                        "amount": None,
                        "unit": Unit.emissions_mass,
                        "description": None,
                    },
                    "passengers": {
                        "amount": None,
                        "unit": Unit.emissions_mass,
                        "description": None,
                    },
                    "freight": {
                        "amount": None,
                        "unit": Unit.emissions_mass,
                        "description": None,
                    },
                },
            },
        },
        "time_metrics": {
            "annual_total_time_spent_at_sea": {
                "amount": None,
                "unit": Unit.hour,
                "description": None,
            },
            "total_time_spent_at_sea": {
                "amount": None,
                "unit": Unit.hour,
                "description": None,
            },
            "total_time_spent_at_sea_through_ice": {
                "amount": None,
                "unit": Unit.hour,
                "description": None,
            },
        },
        "distance_metrics": {
            "distance_travelled_through_ice": {
                "amount": None,
                "unit": Unit.nautical_mile,
                "description": None,
            }
        },
        "density_metrics": {
            "average_cargo_density": {
                "amount": None,
                "unit": Unit.density,
                "description": None,
            }
        },
        "additional_information": None,
    }
