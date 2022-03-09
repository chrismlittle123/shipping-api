import json
import logging

import requests
from aws_lambda_powertools.utilities.typing import LambdaContext

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def create_vessel_item(raw_vessel_data: dict) -> dict:
    return {
        "imo_number": raw_vessel_data["imo_number"],
        "name": "ASTORIA",
        "ship_type": "Passenger ship",
        "reporting_period": 2018,
        "technical_efficiency": None,
        "port_of_registry": None,
        "home_port": None,
        "ice_class": None,
        "doc_issue_date": "2019-02-05",
        "doc_expiry_date": "2020-06-30",
        "verifier_details": {
            "verifier_number": None,
            "verifier_name": "ICS VERIFICATION SERVICES SINGLE MEMBER P.C.",
            "verifier_accreditation_body": "HELLENIC ACCREDITATION SYSTEM (ESYD)",
            "verifier_address": "55 FILONOS STR.\\n185 35 PIRAEUS, GREECE",
            "verifier_city": "PIRAEUS",
            "verifier_accreditation_number": "1101",
            "verifier_country": "GREECE",
        },
        "monitoring_methods": {
            "a": {
                "value": "Yes",
                "description": "BDN and period stock takes of fuel tanks",
            },
            "b": {"value": None, "description": "Bunker fuel tank monitoring on-board"},
            "c": {
                "value": None,
                "description": "Flow meters for applicable combustion processes",
            },
            "d": {"value": None, "description": "Direct CO2 emissions measurement"},
        },
        "fuel_consumption_metrics": {
            "all_voyages": {
                "total": {"value": 6307.75, "unit": "metric tonnes"},
                "annual_average": {
                    "per_distance": {"value": None, "unit": "kilogram / nautical mile"},
                    "per_transport_work": {
                        "mass": {
                            "value": None,
                            "unit": "gram / (metric tonne * nautical mile)",
                        },
                        "volume": {
                            "value": None,
                            "unit": "gram / (meter^3 * nautical mile)",
                        },
                        "deadweight_tonnage": {
                            "value": None,
                            "unit": "gram / (metric tonne * nautical mile)",
                        },
                        "passengers": {
                            "value": None,
                            "unit": "gram / (metric tonne * nautical mile)",
                        },
                        "freight": {
                            "value": None,
                            "unit": "gram / (metric tonne * nautical mile)",
                        },
                    },
                },
                "laden_voyages": {
                    "total": {"value": 6307.75, "unit": "metric tonnes"},
                    "annual_average": {
                        "per_distance": {
                            "value": None,
                            "unit": "kilogram / nautical mile",
                        },
                        "per_transport_work": {
                            "mass": {
                                "value": None,
                                "unit": "gram / (metric tonne * nautical mile)",
                            },
                            "volume": {
                                "value": None,
                                "unit": "gram / (meter^3 * nautical mile)",
                            },
                            "deadweight_tonnage": {
                                "value": None,
                                "unit": "gram / (metric tonne * nautical mile)",
                            },
                            "passengers": {
                                "value": None,
                                "unit": "gram / (metric tonne * nautical mile)",
                            },
                            "freight": {
                                "value": None,
                                "unit": "gram / (metric tonne * nautical mile)",
                            },
                        },
                    },
                },
            },
            "co2_emissions_metrics": {
                "all_voyages": {
                    "total": {"value": 20080.25, "unit": "metric tonnes"},
                    "between_ports": {
                        "value": 16035.42,
                        "unit": "metric tonnes",
                        "description": "CO2 emissions from all voyages between ports under a Member State jurisdiction",
                    },
                    "departed_from_ports": {
                        "value": 728.59,
                        "unit": "metric tonnes",
                        "description": "CO2 emissions from all voyages which departed from ports under a Member State jurisdiction",
                    },
                    "to_ports": {
                        "value": 974.78,
                        "unit": "metric tonnes",
                        "description": "CO2 emissions from all voyages to ports under a Member State jurisdiction",
                    },
                    "within_ports_at_berth": {
                        "value": 2341.47,
                        "unit": "metric tonnes",
                        "description": "CO2 emissions which occurred within ports under a Member State jurisdiction at berth",
                    },
                    "passenger_transport": {"value": None, "unit": "metric tonnes"},
                    "freight_transport": {"value": None, "unit": "metric tonnes"},
                    "annual_average": {
                        "per_distance": {
                            "value": None,
                            "unit": "kilogram / nautical mile",
                        },
                        "per_transport_work": {
                            "mass": {
                                "value": None,
                                "unit": "gram / (metric tonne * nautical mile)",
                            },
                            "volume": {
                                "value": None,
                                "unit": "gram / (meter^3 * nautical mile)",
                            },
                            "deadweight_tonnage": {
                                "value": None,
                                "unit": "gram / (metric tonne * nautical mile)",
                            },
                            "passengers": {
                                "value": None,
                                "unit": "gram / (metric tonne * nautical mile)",
                            },
                            "freight": {
                                "value": None,
                                "unit": "gram / (metric tonne * nautical mile)",
                            },
                        },
                    },
                },
                "laden_voyages": {
                    "total": {"value": None, "unit": "metric tonnes"},
                    "annual_average": {
                        "per_distance": {
                            "value": None,
                            "unit": "kilogram / nautical mile",
                        },
                        "per_transport_work": {
                            "mass": {
                                "value": None,
                                "unit": "gram / (metric tonne * nautical mile)",
                            },
                            "volume": {
                                "value": None,
                                "unit": "gram / (meter^3 * nautical mile)",
                            },
                            "deadweight_tonnage": {
                                "value": None,
                                "unit": "gram / (metric tonne * nautical mile)",
                            },
                            "passengers": {
                                "value": None,
                                "unit": "gram / (metric tonne * nautical mile)",
                            },
                            "freight": {
                                "value": None,
                                "unit": "gram / (metric tonne * nautical mile)",
                            },
                        },
                    },
                },
            },
        },
        "time_metrics": {
            "annual_total_time_spent_at_sea": {"value": 4170.2, "unit": "hour"},
            "total_time_spent_at_sea": {"value": 4170.2, "unit": "hour"},
            "total_time_spent_at_sea_through_ice": {"value": 4170.2, "unit": "hour"},
        },
        "distance_metrics": {
            "distance_travelled_through_ice": {"value": None, "unit": "nautical miles"}
        },
        "density_metrics": {
            "average_cargo_density": {"value": None, "unit": "metric tonnes / m^3"}
        },
        "additional_information": None,
    }


def get_urls() -> dict:
    return {"cinch": "https://www.cinch.co.uk/"}


def handler(event: dict, context: LambdaContext) -> dict:
    urls = get_urls()
    sample_url = urls["cinch"]
    resp = requests.get(sample_url)
    LOGGER.info({"message": "Response", "content": resp})
    return {
        "statusCode": resp.status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"response": resp.text}),
    }
