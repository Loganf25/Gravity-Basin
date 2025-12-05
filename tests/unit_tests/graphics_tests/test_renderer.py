"""Unit tests for renderer class"""
import pytest
import OpenGL.GL as gl
from src.graphics.renderer import Renderer
from src.graphics.texture_loader import TextureLoader
from src.simulation.services.physics_service import PhysicsService
from src.graphics.camera import Camera
from src.simulation.data.simulation_data import PLANET_DATA

class TestRenderer:
    "Tests for renderer.py"

    @pytest.fixture
    def renderer(self):
        "Creates body to use in tests"
        return Renderer(TextureLoader())

    def runUnitTests(self):
        #


