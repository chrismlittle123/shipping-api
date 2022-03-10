import csv
import json
import logging
import os
import re
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Callable, List, Optional, Union

import boto3
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.data_ingestion.pydantic_models import VesselItem

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def clean_null_values(value: Union[str, int, float]) -> Union[str, int, float, None]:
    if str(value).lower().strip() in ["", "n/a", "not applicable"]:
        return None
    return value


def clean_column(column: str) -> str:
    column = re.sub(r"[^a-zA-Z]+", "_", column)
    column = re.sub(r"_{2,}", "", column)
    column = re.sub(r"_$", "", column)
    return column.lower()


def clean_numerical_data(value: Union[str, int, float]) -> Optional[float]:
    try:
        return round(float(value), 2)
    except (ValueError, TypeError):
        return None


def convert_date(date_raw: str) -> Optional[str]:
    try:
        date_object = datetime.strptime(date_raw, "%d/%m/%Y").date()
        date_string = datetime.strftime(date_object, "%Y-%m-%d")
        return date_string
    except ValueError:
        return None


def clean_monitoring_methods(value: Optional[str]) -> str:
    if value == "" or value is None:
        return "No"
    return value.strip()


def extract_technical_efficiency(technical_efficiency: str) -> Optional[float]:
    try:
        extracted_value = re.findall(r"\d*\.?\d+", technical_efficiency)[0]
        return round(float(extracted_value), 2)
    except IndexError:
        return None


def read_csv_from_s3(event: dict) -> Union[List[list], None]:

    s3_client = boto3.client("s3")

    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        content = response["Body"].read().decode("utf-8").splitlines(True)
        csv_reader = csv.reader(content, delimiter=",")
        return [row for row in csv_reader]
    except Exception as error:
        LOGGER.error(
            {"message": "Error when reading CSV file from S3", "content": error}
        )
        return None


def convert_csv_to_dictionaries(csv_content: List[list]) -> List[dict]:
    columns = [clean_column(col) for col in csv_content[0]]
    return [dict(zip(columns, row)) for row in csv_content[1:]]


# TO DO: Create a pydantic model which is used to build the vessel item
# TO DO: Create a generator that writes VesselItem Object to dynamoDB
# TO DO: Write unit tests
# TO DO: Write integration test


def apply_cleaning_function(
    dictionary_input: dict, columns: list, cleaning_function: Callable
) -> dict:
    for col in columns:
        dictionary_input[col] = cleaning_function(dictionary_input[col])
    return dictionary_input


def load_column_type_mappings() -> dict:

    path_list: List[str] = [
        str(Path(__file__).parents[2]),
        "data",
        "config",
        "column_type_mappings.json",
    ]

    column_type_mappings_path = os.path.join(*path_list)

    with open(column_type_mappings_path, "r") as file:
        column_type_mappings = json.load(file)

    return column_type_mappings


def clean_raw_vessel_data(vessel_data_raw: dict, column_type_mappings: dict) -> dict:

    vessel_data_raw = apply_cleaning_function(
        vessel_data_raw, column_type_mappings["float_columns"], clean_numerical_data
    )

    vessel_data_raw = apply_cleaning_function(
        vessel_data_raw, column_type_mappings["upper_case_columns"], lambda x: x.upper()
    )

    vessel_data_raw = apply_cleaning_function(
        vessel_data_raw, column_type_mappings["date_columns"], convert_date
    )

    vessel_data_raw = apply_cleaning_function(
        vessel_data_raw, ["a", "b", "c", "d"], clean_monitoring_methods
    )

    vessel_data_raw = apply_cleaning_function(
        vessel_data_raw, ["technical_efficiency"], extract_technical_efficiency
    )

    vessel_data_raw = apply_cleaning_function(
        vessel_data_raw, ["reporting_period"], int
    )

    vessel_data_raw = apply_cleaning_function(
        vessel_data_raw, list(vessel_data_raw.keys()), clean_null_values
    )

    return vessel_data_raw


def create_vessel_item(vessel_data: dict) -> dict:
    return {
        "imo_number": vessel_data["imo_number"],
        "name": vessel_data["name"],
        "ship_type": vessel_data["ship_type"],
        "reporting_period": vessel_data["reporting_period"],
        "technical_efficiency": vessel_data["technical_efficiency"],
        "port_of_registry": vessel_data["port_of_registry"],
        "home_port": vessel_data["home_port"],
        "ice_class": vessel_data["ice_class"],
        "doc_issue_date": vessel_data["doc_issue_date"],
        "doc_expiry_date": vessel_data["doc_expiry_date"],
        "verifier_details": {
            "verifier_number": vessel_data["verifier_number"],
            "verifier_name": vessel_data["verifier_name"],
            "verifier_accreditation_body": vessel_data["verifier_nab"],
            "verifier_address": vessel_data["verifier_address"],
            "verifier_city": vessel_data["verifier_city"],
            "verifier_accreditation_number": vessel_data[
                "verifier_accreditation_number"
            ],
            "verifier_country": vessel_data["verifier_country"],
        },
        "monitoring_methods": {
            "a": {
                "value": vessel_data["a"],
                "description": "BDN and period stock takes of fuel tanks",
            },
            "b": {
                "value": vessel_data["b"],
                "description": "Bunker fuel tank monitoring on-board",
            },
            "c": {
                "value": vessel_data["c"],
                "description": "Flow meters for applicable combustion processes",
            },
            "d": {
                "value": vessel_data["d"],
                "description": "Direct CO2 emissions measurement",
            },
        },
        "fuel_consumption_metrics": {
            "all_voyages": {
                "total": {
                    "value": vessel_data["total_fuel_consumption_m_tonnes"],
                    "unit": "metric tonne",
                },
                "annual_average": {
                    "per_distance": {
                        "value": vessel_data[
                            "annual_average_fuel_consumption_per_distance_kg_n_mile"
                        ],
                        "unit": "kilogram / nautical mile",
                    },
                    "per_transport_work": {
                        "mass": {
                            "value": vessel_data[
                                "annual_average_fuel_consumption_per_transport_work_mass_g_m_tonnes_n_miles"
                            ],
                            "unit": "gram / (metric tonne * nautical mile)",
                        },
                        "volume": {
                            "value": vessel_data[
                                "annual_average_fuel_consumption_per_transport_work_volume_g_m_n_miles"
                            ],
                            "unit": "gram / (meter^3 * nautical mile)",
                        },
                        "deadweight_tonnage": {
                            "value": vessel_data[
                                "annual_average_fuel_consumption_per_transport_work_dwt_g_dwt_carried_n_miles"
                            ],
                            "unit": "gram / (metric tonne * nautical mile)",
                        },
                        "passengers": {
                            "value": vessel_data[
                                "annual_average_fuel_consumption_per_transport_work_pax_g_pax_n_miles"
                            ],
                            "unit": "gram / (metric tonne * nautical mile)",
                        },
                        "freight": {
                            "value": vessel_data[
                                "fuel_consumption_per_transport_work_freight_on_laden_voyages_g_m_tonnes_n_miles"
                            ],
                            "unit": "gram / (metric tonne * nautical mile)",
                        },
                    },
                },
            },
            "laden_voyages": {
                "total": {
                    "value": vessel_data[
                        "fuel_consumptions_assigned_to_on_laden_m_tonnes"
                    ],
                    "unit": "metric tonne",
                },
                "per_distance": {
                    "value": vessel_data[
                        "fuel_consumption_per_distance_on_laden_voyages_kg_n_mile"
                    ],
                    "unit": "kilogram / nautical mile",
                },
                "per_transport_work": {
                    "mass": {
                        "value": vessel_data[
                            "fuel_consumption_per_transport_work_mass_on_laden_voyages_g_m_tonnes_n_miles"
                        ],
                        "unit": "gram / (metric tonne * nautical mile)",
                    },
                    "volume": {
                        "value": vessel_data[
                            "fuel_consumption_per_transport_work_volume_on_laden_voyages_g_m_n_miles"
                        ],
                        "unit": "gram / (meter^3 * nautical mile)",
                    },
                    "deadweight_tonnage": {
                        "value": vessel_data[
                            "fuel_consumption_per_transport_work_dwt_on_laden_voyages_g_dwt_carried_n_miles"
                        ],
                        "unit": "gram / (metric tonne * nautical mile)",
                    },
                    "passengers": {
                        "value": vessel_data[
                            "fuel_consumption_per_transport_work_pax_on_laden_voyages_g_pax_n_miles"
                        ],
                        "unit": "gram / (metric tonne * nautical mile)",
                    },
                    "freight": {
                        "value": vessel_data[
                            "fuel_consumption_per_transport_work_pax_on_laden_voyages_g_pax_n_miles"
                        ],
                        "unit": "gram / (metric tonne * nautical mile)",
                    },
                },
            },
        },
        "co2_emissions_metrics": {
            "all_voyages": {
                "total": {
                    "value": vessel_data["total_co_emissions_m_tonnes"],
                    "unit": "metric tonne",
                },
                "between_ports": {
                    "value": vessel_data[
                        "co_emissions_from_all_voyages_between_ports_under_a_ms_jurisdiction_m_tonnes"
                    ],
                    "unit": "metric tonne",
                    "description": "CO2 emissions from all voyages between ports under a Member State jurisdiction",
                },
                "departed_from_ports": {
                    "value": vessel_data[
                        "co_emissions_from_all_voyages_which_departed_from_ports_under_a_ms_jurisdiction_m_tonnes"
                    ],
                    "unit": "metric tonne",
                    "description": "CO2 emissions from all voyages which departed from ports under a Member State jurisdiction",
                },
                "to_ports": {
                    "value": vessel_data[
                        "co_emissions_from_all_voyages_to_ports_under_a_ms_jurisdiction_m_tonnes"
                    ],
                    "unit": "metric tonne",
                    "description": "CO2 emissions from all voyages to ports under a Member State jurisdiction",
                },
                "within_ports_at_berth": {
                    "value": vessel_data[
                        "co_emissions_which_occurred_within_ports_under_a_ms_jurisdiction_at_berth_m_tonnes"
                    ],
                    "unit": "metric tonne",
                    "description": "CO2 emissions which occurred within ports under a Member State jurisdiction at berth",
                },
                "passenger_transport": {
                    "value": vessel_data[
                        "co_emissions_assigned_to_passenger_transport_m_tonnes"
                    ],
                    "unit": "metric tonne",
                },
                "freight_transport": {
                    "value": vessel_data[
                        "co_emissions_assigned_to_freight_transport_m_tonnes"
                    ],
                    "unit": "metric tonne",
                },
                "annual_average": {
                    "per_distance": {
                        "value": vessel_data[
                            "annual_average_co_emissions_per_distance_kg_co_n_mile"
                        ],
                        "unit": "kilogram / nautical mile",
                    },
                    "per_transport_work": {
                        "mass": {
                            "value": vessel_data[
                                "annual_average_co_emissions_per_transport_work_mass_g_co_m_tonnes_n_miles"
                            ],
                            "unit": "gram / (metric tonne * nautical mile)",
                        },
                        "volume": {
                            "value": vessel_data[
                                "annual_average_co_emissions_per_transport_work_volume_g_co_m_n_miles"
                            ],
                            "unit": "gram / (meter^3 * nautical mile)",
                        },
                        "deadweight_tonnage": {
                            "value": vessel_data[
                                "annual_average_co_emissions_per_transport_work_dwt_g_co_dwt_carried_n_miles"
                            ],
                            "unit": "gram / (metric tonne * nautical mile)",
                        },
                        "passengers": {
                            "value": vessel_data[
                                "annual_average_co_emissions_per_transport_work_pax_g_co_pax_n_miles"
                            ],
                            "unit": "gram / (metric tonne * nautical mile)",
                        },
                        "freight": {
                            "value": vessel_data[
                                "annual_average_co_emissions_per_transport_work_freight_g_co_m_tonnes_n_miles"
                            ],
                            "unit": "gram / (metric tonne * nautical mile)",
                        },
                    },
                },
            },
            "laden_voyages": {
                "total": {
                    "value": vessel_data["co_emissions_assigned_to_on_laden_m_tonnes"],
                    "unit": "metric tonne",
                },
                "per_distance": {
                    "value": vessel_data[
                        "co_emissions_per_distance_on_laden_voyages_kg_co_n_mile"
                    ],
                    "unit": "kilogram / nautical mile",
                },
                "per_transport_work": {
                    "mass": {
                        "value": vessel_data[
                            "co_emissions_per_transport_work_mass_on_laden_voyages_g_co_m_tonnes_n_miles"
                        ],
                        "unit": "gram / (metric tonne * nautical mile)",
                    },
                    "volume": {
                        "value": vessel_data[
                            "co_emissions_per_transport_work_volume_on_laden_voyages_g_co_m_n_miles"
                        ],
                        "unit": "gram / (meter^3 * nautical mile)",
                    },
                    "deadweight_tonnage": {
                        "value": vessel_data[
                            "co_emissions_per_transport_work_dwt_on_laden_voyages_g_co_dwt_carried_n_miles"
                        ],
                        "unit": "gram / (metric tonne * nautical mile)",
                    },
                    "passengers": {
                        "value": vessel_data[
                            "co_emissions_per_transport_work_pax_on_laden_voyages_g_co_pax_n_miles"
                        ],
                        "unit": "gram / (metric tonne * nautical mile)",
                    },
                    "freight": {
                        "value": vessel_data[
                            "co_emissions_per_transport_work_freight_on_laden_voyages_g_co_m_tonnes_n_miles"
                        ],
                        "unit": "gram / (metric tonne * nautical mile)",
                    },
                },
            },
        },
        "time_metrics": {
            "annual_total_time_spent_at_sea": {
                "value": vessel_data["annual_total_time_spent_at_sea_hours"],
                "unit": "hour",
            },
            "total_time_spent_at_sea": {
                "value": vessel_data["total_time_spent_at_sea_hours"],
                "unit": "hour",
            },
            "total_time_spent_at_sea_through_ice": {
                "value": vessel_data["total_time_spent_at_sea_through_ice_hours"],
                "unit": "hour",
            },
        },
        "distance_metrics": {
            "distance_travelled_through_ice": {
                "value": vessel_data["through_ice_n_miles"],
                "unit": "nautical mile",
            }
        },
        "density_metrics": {
            "average_cargo_density": {
                "value": vessel_data[
                    "average_density_of_the_cargo_transported_m_tonnes_m"
                ],
                "unit": "metric tonne / meter^3",
            }
        },
        "additional_information": vessel_data[
            "additional_information_to_facilitate_the_understanding_of_the_reported_average_operational_energy_efficiency_indicators"
        ],
    }


def process_raw_vessel_data(vessel_data_raw: dict, column_type_mappings: dict) -> dict:

    vessel_data = clean_raw_vessel_data(vessel_data_raw, column_type_mappings)
    vessel_item = create_vessel_item(vessel_data)
    vessel_item_object = VesselItem(**vessel_item)

    return json.loads(vessel_item_object.json())


def main(event: dict) -> Optional[List[dict]]:

    csv_content = read_csv_from_s3(event)
    column_type_mappings = load_column_type_mappings()

    if csv_content:
        vessel_data_raw_dictionaries = convert_csv_to_dictionaries(csv_content)

        vessel_list = []

        for vessel_data_raw in vessel_data_raw_dictionaries:

            vessel_item_object = process_raw_vessel_data(
                vessel_data_raw, column_type_mappings
            )
            vessel_list.append(vessel_item_object)

        return vessel_list
    return None


def handler(event: dict, context: LambdaContext) -> dict:
    LOGGER.info({"message": "Incoming event", "content": json.dumps(event)})
    vessel_list = main(event)

    if vessel_list:
        return {"body": json.dumps(vessel_list[0])}
    return {"body": None}
