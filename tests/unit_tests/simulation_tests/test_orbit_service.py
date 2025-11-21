"""Unit Tests for the orbit_service class"""
import pytest
from src.simulation.services.orbit_service import OrbitService
from src.simulation.models.planet import Planet


class TestOrbitService:
    "Tests for orbit_service.py"

    @pytest.fixture
    def orbit_service(self):
        "Creates body to use in tests"
        return OrbitService()

    def test_compute_orbit(self, orbit_service):
        "Tests the compute_orbit function of orbit_service"
        body1 = Planet("Earth")
        body2 = Planet("Sun")
        AU_VISUAL_SCALE = 1.0
        orbit_params = orbit_service.compute_orbit(body1, body2, AU_VISUAL_SCALE)
        assert orbit_params is not None
        assert "distance" in orbit_params
        assert "orbital_velocity" in orbit_params
        assert orbit_params["distance"] > 0
        assert orbit_params["orbital_velocity"] > 0



