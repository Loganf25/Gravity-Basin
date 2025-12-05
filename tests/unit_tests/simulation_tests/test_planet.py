"""Unit tests for the Planet class."""
import pytest
from src.simulation.models.planet import Planet

class TestPlanet:
    "Tests for Celestial Body class"

    @pytest.fixture
    def planet(self):
        "Creates body to use in tests"
        return Planet(
            name="Earth"
        )

    def test_init(self, planet):
        "Tests the initialization of planet"
        assert planet.name == "Earth"
        assert planet.mass == 5.97237e24
        assert planet.radius == 0.0042
        assert planet.distance == 1.0
        assert planet.color == (0.2, 0.5, 1.0)          #Red
        assert planet.texture == "earth.jpg"
        assert planet.axial_tilt == 23.4
        assert planet.rotation_speed == 360.0 / (23.9 * 3600.0)
        assert planet.eccentricity == 0.017

    def test_update(self, planet):
        "Tests the update function of planet"
        initial_angle = planet.rotation_angle
        delta_time = 1.0
        planet.update(delta_time)
        expected_angle = (initial_angle + planet.rotation_speed * delta_time) % 360.0
        assert planet.rotation_angle == pytest.approx(expected_angle)

    def runUnitTests(self):
        self.test_init(self.planet())
        self.test_update(self.planet())