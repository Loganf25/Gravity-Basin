"""Unit tests for physics service class"""
import pytest
from src.simulation.services.physics_service import PhysicsService
from src.simulation.models.planet import Planet

class TestPhysicsService:
    "Tests for physics_service.py"
    
    @pytest.fixture
    def physics_service(self):
        "Creates body to use in tests"
        return PhysicsService()

    def test_compute_gravitational_force(self, physics_service):
        "Tests the compute_gravitational_force function of physics_service"
        body1 = Planet("Earth")
        body2 = Planet("Sun")
        force_vector = physics_service.compute_gravitational_force(body1, body2)
        assert force_vector is not None
        assert force_vector[0] > 0
        assert force_vector[1] > 0
        assert force_vector[2] > 0

    def test_step(self, physics_service):
        "Tests the step function of physics_service"
        body1 = Planet("Earth")
        body2 = Planet("Sun")
        physics_service.register_body(body1)
        physics_service.register_body(body2)
        delta_time = 1.0
        physics_service.step(delta_time)
        assert body1.position[0] > 0
        assert body1.position[1] > 0
        assert body1.position[2] > 0
        assert body1.velocity[0] > 0
        assert body1.velocity[1] > 0
        assert body1.velocity[2] > 0

    def test_register_body(self, physics_service):
        "Tests the register_body function of physics_service"
        body1 = Planet("Earth")
        physics_service.register_body(body1)
        assert body1 in physics_service.bodies

    def test_clear_bodies(self, physics_service):
        "Tests the clear_bodies function of physics_service"
        body1 = Planet("Earth")
        physics_service.register_body(body1)
        physics_service.clear_bodies()
        assert len(physics_service.bodies) == 0

    def runUnitTests(self):
        self.test_compute_gravitational_force(self.physics_service)
        self.test_step(self.physics_service)
        self.test_register_body(self.physics_service)
        self.test_clear_bodies(self.physics_service)