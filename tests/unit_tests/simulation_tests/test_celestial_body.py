"""Unit tests for the CelestialBody class."""
import pytest
from src.simulation.models.celestial_body import CelestialBody

class TestCelestialBody:
    "Tests for Celestial Body class"

    @pytest.fixture
    def celestial_body(self):
        "Creates body to use in tests"
        return CelestialBody(
            name="Test Body",
            mass=100.0,
            radius=10.0,
            distance=1000.0,
            color=(1.0, 0.0, 0.0),
            texture="test_texture.jpg",
            axial_tilt=0.0
        )

    def test_init(self, celestial_body):
        "Tests the initialization of celestial_body"
        assert celestial_body.name == "Test Body"
        assert celestial_body.mass == 100.0
        assert celestial_body.radius == 10.0
        assert celestial_body.distance == 1000.0
        assert celestial_body.color == (1.0, 0.0, 0.0)          #Red
        assert celestial_body.texture == "test_texture.jpg"
        assert celestial_body.axial_tilt == 0.0
        assert celestial_body.position == [1000.0, 0.0, 0.0]
        assert celestial_body.velocity == [0.0, 0.0, 0.0]
        assert celestial_body.rotation_speed == 5.0             #Default
        assert celestial_body.rotation_angle == 0.0

    def test_update(self, celestial_body):
        "Tests the update function of celestial_body"
        initial_angle = celestial_body.rotation_angle
        delta_time = 1.0
        celestial_body.update(delta_time)
        expected_angle = (initial_angle + celestial_body.rotation_speed * delta_time) % 360.0
        assert celestial_body.rotation_angle == pytest.approx(expected_angle)

    def test_tick_rotation(self, celestial_body):
        "Tests the tick_rotation function of celestial_body"
        delta_time = 1.0 #Adds 5 dgrees to rotation_angle
        celestial_body.tick_rotation(delta_time)
        assert celestial_body.rotation_angle == pytest.approx(5)
        celestial_body.tick_rotation(delta_time)
        assert celestial_body.rotation_angle == pytest.approx(10)

    def test_tick_rotation_end_rotation(self, celestial_body):
        """Tests the tick_rotation function of celestial_body at the end of a full rotation"""
        celestial_body.rotation_angle = 359.0
        delta_time = 1.0 #Adds 5 degress tro rotation_angle
        celestial_body.tick_rotation(delta_time)
        assert celestial_body.rotation_angle == pytest.approx(4.0)