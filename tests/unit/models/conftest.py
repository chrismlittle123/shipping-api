import os

import boto3
import pytest
from moto import mock_dynamodb


@pytest.fixture()
def aws_credentials(mocker):
    """Mocked AWS Credentials for moto."""
    mocker.patch.dict(
        os.environ,
        {
            "AWS_REGION": "eu-west-2",
            "AWS_ACCESS_KEY_ID": "testing",
            "AWS_SECRET_ACCESS_KEY": "testing",
            "AWS_SECURITY_TOKEN": "testing",
            "AWS_SESSION_TOKEN": "testing",
        },
    )


@pytest.fixture()
def shipping_data_table():
    with mock_dynamodb():

        dynamodb = boto3.resource("dynamodb", "eu-west-2")

        table = dynamodb.create_table(
            TableName="shipping-data",
            KeySchema=[
                {"AttributeName": "PK", "KeyType": "HASH"},
                {"AttributeName": "SK", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "PK", "AttributeType": "S"},
                {"AttributeName": "SK", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 25, "WriteCapacityUnits": 25},
        )

        yield table

        table.delete()


@pytest.fixture()
def sample_vessel_item():
    return {
        "pk": "EU_MRV_EMISSIONS_DATA",
        "sk": "REPORTING_PERIOD#2018#IMO_NUMBER#5383304",
        "updated_date": "2021-07-30 09:00:00",
        "imo_number": "5383304",
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
            "verifier_address": "55 FILONOS STR.\n185 35 PIRAEUS, GREECE",
            "verifier_city": "PIRAEUS",
            "verifier_accreditation_number": "1101",
            "verifier_country": "GREECE",
        },
        "monitoring_methods": {
            "a": {
                "value": "Yes",
                "description": "BDN and period stock takes of fuel tanks",
            },
            "b": {"value": "No", "description": "Bunker fuel tank monitoring on-board"},
            "c": {
                "value": "No",
                "description": "Flow meters for applicable combustion processes",
            },
            "d": {"value": "No", "description": "Direct CO2 emissions measurement"},
        },
        "fuel_consumption_metrics": {
            "all_voyages": {
                "total": {"value": 6307.75, "unit": "metric tonne"},
                "annual_average": {
                    "per_distance": {
                        "value": 139.07,
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
                            "value": 311.97,
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
                "total": {"value": None, "unit": "metric tonne"},
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
        },
        "co2_emissions_metrics": {
            "all_voyages": {
                "total": {"value": 20080.25, "unit": "metric tonne"},
                "between_ports": {
                    "value": 16035.42,
                    "unit": "metric tonne",
                    "description": "CO2 emissions from all voyages between ports under a Member State jurisdiction",
                },
                "departed_from_ports": {
                    "value": 728.59,
                    "unit": "metric tonne",
                    "description": "CO2 emissions from all voyages which departed from ports under a Member State jurisdiction",
                },
                "to_ports": {
                    "value": 974.78,
                    "unit": "metric tonne",
                    "description": "CO2 emissions from all voyages to ports under a Member State jurisdiction",
                },
                "within_ports_at_berth": {
                    "value": 2341.47,
                    "unit": "metric tonne",
                    "description": "CO2 emissions which occurred within ports under a Member State jurisdiction at berth",
                },
                "passenger_transport": {"value": None, "unit": "metric tonne"},
                "freight_transport": {"value": None, "unit": "metric tonne"},
                "annual_average": {
                    "per_distance": {
                        "value": 442.71,
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
                            "value": 993.14,
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
                "total": {"value": None, "unit": "metric tonne"},
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
        },
        "time_metrics": {
            "annual_total_time_spent_at_sea": {"value": 4170.2, "unit": "hour"},
            "total_time_spent_at_sea": {"value": 4170.2, "unit": "hour"},
            "total_time_spent_at_sea_through_ice": {"value": None, "unit": "hour"},
        },
        "distance_metrics": {
            "distance_travelled_through_ice": {"value": None, "unit": "nautical mile"}
        },
        "density_metrics": {
            "average_cargo_density": {"value": None, "unit": "metric tonne / meter^3"}
        },
        "additional_information": None,
    }
