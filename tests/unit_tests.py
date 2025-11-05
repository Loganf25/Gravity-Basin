"""Unit tests for the Universe Simulator"""
from types import SimpleNamespace
from src.simulation.services.physics_service import PhysicsService

## !!!!!! TEST TESTS FOR PHYSICS SERVICE !!!!! ##
## Follow this sort of function structure for other tests ##


def test_compute_gravitational_force_direction():
    """Test that gravitational force direction is correct between two bodies."""
    ps = PhysicsService()
    b1 = SimpleNamespace(position=[0.0, 0.0, 0.0], mass=5.0)
    b2 = SimpleNamespace(position=[1.0, 0.0, 0.0], mass=5.0)

    f = ps.compute_gravitational_force(b1, b2)

    assert isinstance(f, list)
    assert len(f) == 3
    # b2 is at +x relative to b1, so force on b1 should be +x
    assert f[0] > 0
    assert abs(f[1]) < 1e-12
    assert abs(f[2]) < 1e-12


def test_step_updates_velocity_and_position():
    """Test that the step function updates velocities and positions of bodies."""
    ps = PhysicsService()

    b1 = SimpleNamespace(position=[0.0, 0.0, 0.0], mass=5.0, velocity=[0.0, 0.0, 0.0], trail=[])
    b2 = SimpleNamespace(position=[1.0, 0.0, 0.0], mass=5.0, velocity=[0.0, 0.0, 0.0], trail=[])

    ps.bodies = [b1, b2]

    # Run a single physics step
    ps.step(1.0)

    # At least one body's velocity should change from 0
    changed = any(abs(v) > 0.0 for v in b1.velocity) or any(abs(v) > 0.0 for v in b2.velocity)
    assert changed

    # Position values should remain lists and be updated numerically
    assert isinstance(b1.position, list)
    assert isinstance(b2.position, list)
