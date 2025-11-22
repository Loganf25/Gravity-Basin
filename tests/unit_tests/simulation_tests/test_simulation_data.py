"""Unit tests for the simulation_data file"""
import pytest
from src.simulation.data.simulation_data import get_planet_data

class TestSimulationData:
    "Tests for simulation_data.py"

    @pytest.fixture
    def test_get_planet_data_valid(self):
        "Tests that get_planet_data returns the correct data for a valid planet name"
        earth_data = get_planet_data("Earth")
        assert earth_data is not None
        assert earth_data["name"] == "Earth"
        assert earth_data["mass"] == 5.97237e24

    def test_get_planet_data_invalid(self):
        "Tests that get_planet_data returns None for an invalid planet name"
        invalid_data = get_planet_data("InvalidPlanet")
        assert invalid_data is None

    def test_get_planet_data_case_insensitivity(self):
        "Tests that get_planet_data is case-insensitive"
        mercury_data_lower = get_planet_data("mercury")
        mercury_data_upper = get_planet_data("MERCURY")
        assert mercury_data_lower is not None
        assert mercury_data_upper is not None
        assert mercury_data_lower["name"] == "Mercury"
        assert mercury_data_upper["name"] == "Mercury"
