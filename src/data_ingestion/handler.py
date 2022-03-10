import csv
import json
import logging
import re
import urllib.parse
from datetime import datetime
from typing import Callable, List, Union

import boto3
from aws_lambda_powertools.utilities.typing import LambdaContext

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def make_upper_case(value: str) -> str:
    if isinstance(value, str):
        return value.upper()
    return value


def clean_null_values(value: Union[str, int, float]) -> Union[str, int, float, None]:
    if value == "":
        return None
    return value


def clean_column(column: str) -> str:
    column = re.sub(r"[^a-zA-Z]+", "_", column)
    column = re.sub(r"_{2,}", "", column)
    column = re.sub(r"_$", "", column)
    return column.lower()


def clean_numerical_data(value: Union[str, int, float]) -> Union[float, None]:
    if value == "Division by zero!":
        return None
    try:
        return round(float(value), 2)
    except ValueError:
        return None


def convert_date(date_raw: str) -> Union[str, None]:
    if date_raw == "DoC not issued":
        return None

    date_object = datetime.strptime(date_raw, "%d/%m/%Y").date()
    date_string = datetime.strftime(date_object, "%Y-%m-%d")

    return date_string


def extract_technical_efficiency(technical_efficiency: str) -> Union[float, None]:
    if technical_efficiency == "Not Applicable":
        return None

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
        LOGGER.info({"message": "Error", "content": error})
        return None


def convert_csv_to_dictionaries(csv_content: List[list]) -> List[dict]:
    columns = [clean_column(col) for col in csv_content[0]]
    return [dict(zip(columns, row)) for row in csv_content[1:]]


# TO DO: Create a function which cleans vessel data dictionaries, output the data back as a CSV for inspection
# TO DO: Finish building create_vessel_item function
# TO DO: Create a pydantic model which is used to build the vessel item
# TO DO: Write a function which writes objects to DynamoDB
# TO DO: Write unit tests
# TO DO: Write integration test


def apply_cleaning_function(
    dictionary_input: dict, columns: list, cleaning_function: Callable
) -> dict:
    for col in columns:
        dictionary_input[col] = cleaning_function(dictionary_input[col])
    return dictionary_input


def clean_raw_vessel_data(vessel_data_raw: dict) -> dict:

    columns = vessel_data_raw.keys()

    string_columns = [
        "imo_number",
        "name",
        "ship_type",
        "reporting_period",
        "technical_efficiency",
        "port_of_registry",
        "home_port",
        "ice_class",
        "doc_issue_date",
        "doc_expiry_date",
        "verifier_number",
        "verifier_name",
        "verifier_nab",
        "verifier_address",
        "verifier_city",
        "verifier_accreditation_number",
        "verifier_country",
        "a",
        "b",
        "c",
        "d",
    ]

    float_columns = [col for col in columns if col not in string_columns]
    upper_case_columns = [
        "name",
        "port_of_registry",
        "home_port",
        "verifier_name",
        "verifier_nab",
        "verifier_address",
        "verifier_city",
        "verifier_country",
    ]
    date_columns = ["doc_issue_date", "doc_expiry_date"]

    vessel_data_raw = apply_cleaning_function(
        vessel_data_raw, float_columns, clean_numerical_data
    )

    vessel_data_raw = apply_cleaning_function(
        vessel_data_raw, upper_case_columns, make_upper_case
    )

    vessel_data_raw = apply_cleaning_function(
        vessel_data_raw, date_columns, convert_date
    )

    vessel_data_raw = apply_cleaning_function(
        vessel_data_raw, ["technical_efficiency"], extract_technical_efficiency
    )

    vessel_data_raw = apply_cleaning_function(
        vessel_data_raw, ["reporting_period"], int
    )

    vessel_data_raw = apply_cleaning_function(
        vessel_data_raw, list(columns), clean_null_values
    )

    return vessel_data_raw


def create_vessel_item(vessel_data: dict) -> dict:

    return {
        "imo_number": vessel_data["imo_number"],
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


def main(event: dict) -> Union[List[dict], None]:

    csv_content = read_csv_from_s3(event)
    if csv_content:
        vessel_data_raw_dictionaries = convert_csv_to_dictionaries(csv_content)

        vessel_list = []
        for vessel_data_raw in vessel_data_raw_dictionaries:
            vessel_data = clean_raw_vessel_data(vessel_data_raw)
            vessel_list.append(vessel_data)

        return vessel_list
    return None


def handler(event: dict, context: LambdaContext) -> dict:
    LOGGER.info({"message": "Incoming event", "content": json.dumps(event)})
    vessel_list = main(event)
    return {"body": json.dumps(vessel_list)}
