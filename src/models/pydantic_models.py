import re
from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, validator


class Unit(Enum):
    nautical_mile = "nautical mile"
    metric_tonne = "metric tonne"
    hour = "hour"
    density = "metric tonne / meter^3"
    emissions_mass = "gram / (metric tonne * nautical mile)"
    emissions_volume = "gram / (meter^3 * nautical mile)"
    emissions_distance = "kilogram / nautical mile"


class Boolean(Enum):
    yes = "Yes"
    no = "No"


class Method(BaseModel):
    value: Boolean
    description: str


class Metric(BaseModel):
    value: Optional[float]
    unit: Unit


class MetricWithDescription(BaseModel):
    value: Optional[float]
    unit: Unit
    description: str


class MonitoringMethods(BaseModel):
    a: Method
    b: Method
    c: Method
    d: Method


class VerifierDetails(BaseModel):
    verifier_number: Optional[str]
    verifier_name: str
    verifier_accreditation_body: str
    verifier_address: str
    verifier_city: str
    verifier_accreditation_number: str
    verifier_country: str


class PerTransportWork(BaseModel):
    mass: Metric
    volume: Metric
    deadweight_tonnage: Metric
    passengers: Metric
    freight: Metric


class AnnualAverage(BaseModel):
    per_distance: Metric
    per_transport_work: PerTransportWork


class FuelConsumptionAllVoyages(BaseModel):
    total: Metric
    annual_average: AnnualAverage


class FuelConsumptionLadenVoyages(BaseModel):
    total: Metric
    per_distance: Metric
    per_transport_work: PerTransportWork


class Co2EmissionsAllVoyages(BaseModel):
    total: Metric
    between_ports: MetricWithDescription
    departed_from_ports: MetricWithDescription
    to_ports: MetricWithDescription
    within_ports_at_berth: MetricWithDescription
    passenger_transport: Metric
    freight_transport: Metric
    annual_average: AnnualAverage


class Co2EmissionsLadenVoyages(BaseModel):
    total: Metric
    per_distance: Metric
    per_transport_work: PerTransportWork


class FuelConsumptionMetrics(BaseModel):
    all_voyages: FuelConsumptionAllVoyages
    laden_voyages: FuelConsumptionLadenVoyages


class Co2EmissionsMetrics(BaseModel):
    all_voyages: Co2EmissionsAllVoyages
    laden_voyages: Co2EmissionsLadenVoyages


class TimeMetrics(BaseModel):
    annual_total_time_spent_at_sea: Metric
    total_time_spent_at_sea: Metric
    total_time_spent_at_sea_through_ice: Metric


class DistanceMetrics(BaseModel):
    distance_travelled_through_ice: Metric


class DensityMetrics(BaseModel):
    average_cargo_density: Metric


class VesselItem(BaseModel):
    imo_number: str
    name: str
    ship_type: str
    reporting_period: int
    technical_efficiency: Optional[float]
    port_of_registry: Optional[str]
    home_port: Optional[str]
    ice_class: Optional[str]
    doc_issue_date: Optional[date]
    doc_expiry_date: Optional[date]
    verifier_details: VerifierDetails
    monitoring_methods: MonitoringMethods
    fuel_consumption_metrics: FuelConsumptionMetrics
    co2_emissions_metrics: Co2EmissionsMetrics
    time_metrics: TimeMetrics
    distance_metrics: DistanceMetrics
    density_metrics: DensityMetrics
    additional_information: Optional[str]

    @validator("imo_number")
    @classmethod
    def imo_number_7_digits(cls, value: str) -> Optional[str]:
        if not re.match(r"^\d{7}$", value):
            raise ValueError("IMO Number must be 7 digits long")
        return value
