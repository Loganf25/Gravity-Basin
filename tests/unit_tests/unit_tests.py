"""Unit tests for the Universe Simulator"""
from core_tests.test_engine import EngineTest
from core_tests.test_input_hander import testInputHandler
from core_tests.test_selection_manager import test_selection_manager
from core_tests.test_time_manager import TestTimeManager

from graphics_tests.test_camera import TestCamera
from graphics_tests.test_renderer import TestRenderer
from graphics_tests.test_texture_loader import TestTextureLoader

from simulation_tests.test_celestial_body import TestCelestialBody
from simulation_tests.test_orbit_service import TestOrbitService
from simulation_tests.test_physics_service import TestPhysicsService
from simulation_tests.test_planet import TestPlanet
from simulation_tests.test_simulation_data import TestSimulationData

def unitTests():
    EngineTest.runUnitTests()
    testInputHandler.runUnitTests()
    test_selection_manager.runUnitTests()
    TestTimeManager.runUnitTests()
    
    TestCamera.runUnitTests()
    TestRenderer.runUnitTests()
    TestTextureLoader.runUnitTests()
    
    TestCelestialBody.runUnitTests()
    TestOrbitService.runUnitTests()
    TestPhysicsService.runUnitTests()
    TestPlanet.runUnitTests()
    TestSimulationData.runUnitTests()
