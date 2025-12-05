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
    def testRender(self, renderer):
        renderer.initalize_textures(PLANET_DATA)
        assert renderer.initalized == True

    def runUnitTests(self):
        self.testRenderer(self.renderer())


