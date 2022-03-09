import json
import os
from pathlib import Path

from src.data_ingestion.handler import create_vessel_item, get_urls


def test_create_vessel_item():

    raw_vessel_data = {
        "imo_number": 6602898,
        "name": "OCEAN MAJESTY",
        "ship_type": "Passenger ship",
        "reporting_period": 2020,
        "technical_efficiency": 31.73,
        "port_of_registry": "MADEIRA",
        "home_port": None,
        "ice_class": None,
        "doc_issue_date": "2021-07-01",
        "doc_expiry_date": "2022-06-30",
        "verifier_number": None,
        "verifier_name": "BUREAU VERITAS CERTIFICATION FRANCE",
        "verifier_nab": "COFRAC",
        "verifier_address": "LE TRIANGLE DE L'ARCHE\n9, COURS DU TRIANGLE",
        "verifier_city": "92937 PARIS LA DEFENSE",
        "verifier_accreditation_number": "4-0076",
        "verifier_country": "FRANCE",
        "a": "Yes",
        "b": None,
        "c": None,
        "d": None,
        "total_fuel_consumption_m_tonnes": 951.37,
        "fuel_consumptions_assigned_to_on_laden_m_tonnes": None,
        "total_co_emissions_m_tonnes": 2985.13,
        "co_emissions_from_all_voyages_between_ports_under_a_ms_jurisdiction_m_tonnes": 1505.53,
        "co_emissions_from_all_voyages_which_departed_from_ports_under_a_ms_jurisdiction_m_tonnes": 267.5,
        "co_emissions_from_all_voyages_to_ports_under_a_ms_jurisdiction_m_tonnes": 367.12,
        "co_emissions_which_occurred_within_ports_under_a_ms_jurisdiction_at_berth_m_tonnes": 844.98,
        "co_emissions_assigned_to_passenger_transport_m_tonnes": None,
        "co_emissions_assigned_to_freight_transport_m_tonnes": None,
        "co_emissions_assigned_to_on_laden_m_tonnes": None,
        "annual_total_time_spent_at_sea_hours": 488.87,
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
        "total_time_spent_at_sea_hours": 488.87,
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


def test_true_is_true():
    assert True


def test_get_urls():
    assert get_urls() == {"cinch": "https://www.cinch.co.uk/"}
