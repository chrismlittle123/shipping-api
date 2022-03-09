import json
import os
from pathlib import Path

from src.data_ingestion.handler import create_vessel_item


def test_create_vessel_item():

    raw_vessel_data = {
        "imo_number": 5383304,
        "name": "ASTORIA",
        "ship_type": "Passenger ship",
        "reporting_period": 2018,
        "technical_efficiency": None,
        "port_of_registry": None,
        "home_port": None,
        "ice_class": None,
        "doc_issue_date": "2019-02-05",
        "doc_expiry_date": "2020-06-30",
        "verifier_number": None,
        "verifier_name": "ICS VERIFICATION SERVICES SINGLE MEMBER P.C.",
        "verifier_nab": "HELLENIC ACCREDITATION SYSTEM (ESYD)",
        "verifier_address": "55 FILONOS STR.\n185 35 PIRAEUS, GREECE",
        "verifier_city": "PIRAEUS",
        "verifier_accreditation_number": "1101",
        "verifier_country": "GREECE",
        "a": "Yes",
        "b": None,
        "c": None,
        "d": None,
        "total_fuel_consumption_m_tonnes": 6307.75,
        "fuel_consumptions_assigned_to_on_laden_m_tonnes": None,
        "total_co_emissions_m_tonnes": 20080.25,
        "co_emissions_from_all_voyages_between_ports_under_a_ms_jurisdiction_m_tonnes": 16035.42,
        "co_emissions_from_all_voyages_which_departed_from_ports_under_a_ms_jurisdiction_m_tonnes": 728.59,
        "co_emissions_from_all_voyages_to_ports_under_a_ms_jurisdiction_m_tonnes": 974.78,
        "co_emissions_which_occurred_within_ports_under_a_ms_jurisdiction_at_berth_m_tonnes": 2341.47,
        "co_emissions_assigned_to_passenger_transport_m_tonnes": None,
        "co_emissions_assigned_to_freight_transport_m_tonnes": None,
        "co_emissions_assigned_to_on_laden_m_tonnes": None,
        "annual_total_time_spent_at_sea_hours": 4170.2,
        "annual_average_fuel_consumption_per_distance_kg_n_mile": None,
        "annual_average_fuel_consumption_per_transport_work_mass_g_m_tonnes_n_miles": None,
        "annual_average_fuel_consumption_per_transport_work_volume_g_m_n_miles": None,
        "annual_average_fuel_consumption_per_transport_work_dwt_g_dwt_carried_n_miles": None,
        "annual_average_fuel_consumption_per_transport_work_pax_g_pax_n_miles": None,
        "annual_average_fuel_consumption_per_transport_work_freight_g_m_tonnes_n_miles": None,
        "annual_average_co_emissions_per_distance_kg_co_n_mile": None,
        "annual_average_co_emissions_per_transport_work_mass_g_co_m_tonnes_n_miles": None,
        "annual_average_co_emissions_per_transport_work_volume_g_co_m_n_miles": None,
        "annual_average_co_emissions_per_transport_work_dwt_g_co_dwt_carried_n_miles": None,
        "annual_average_co_emissions_per_transport_work_pax_g_co_pax_n_miles": None,
        "annual_average_co_emissions_per_transport_work_freight_g_co_m_tonnes_n_miles": None,
        "through_ice_n_miles": None,
        "total_time_spent_at_sea_hours": 4170.2,
        "total_time_spent_at_sea_through_ice_hours": None,
        "fuel_consumption_per_distance_on_laden_voyages_kg_n_mile": None,
        "fuel_consumption_per_transport_work_mass_on_laden_voyages_g_m_tonnes_n_miles": None,
        "fuel_consumption_per_transport_work_volume_on_laden_voyages_g_m_n_miles": None,
        "fuel_consumption_per_transport_work_dwt_on_laden_voyages_g_dwt_carried_n_miles": None,
        "fuel_consumption_per_transport_work_pax_on_laden_voyages_g_pax_n_miles": None,
        "fuel_consumption_per_transport_work_freight_on_laden_voyages_g_m_tonnes_n_miles": None,
        "co_emissions_per_distance_on_laden_voyages_kg_co_n_mile": None,
        "co_emissions_per_transport_work_mass_on_laden_voyages_g_co_m_tonnes_n_miles": None,
        "co_emissions_per_transport_work_volume_on_laden_voyages_g_co_m_n_miles": None,
        "co_emissions_per_transport_work_dwt_on_laden_voyages_g_co_dwt_carried_n_miles": None,
        "co_emissions_per_transport_work_pax_on_laden_voyages_g_co_pax_n_miles": None,
        "co_emissions_per_transport_work_freight_on_laden_voyages_g_co_m_tonnes_n_miles": None,
        "additional_information_to_facilitate_the_understanding_of_the_reported_average_operational_energy_efficiency_indicators": None,
        "average_density_of_the_cargo_transported_m_tonnes_m": None,
    }

    json_path = os.path.join(*[Path(__file__).parent, "resources", "vessel_clean.json"])

    with open(json_path) as file:
        vessel_clean = json.load(file)

    assert create_vessel_item(raw_vessel_data) == vessel_clean
