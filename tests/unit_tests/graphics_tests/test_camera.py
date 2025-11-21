"""Unit tests for camera class"""
import pytest
from src.graphics.camera import Camera
from src.core.input_handler import InputHandler


class TestCamera:
    "Tests for camera.py"

    @pytest.fixture
    def camera(self):
        "Creates body to use in tests"
        return Camera()

    def test_handle_input(self, camera):
        "Tests the handle_input function of camera"
        input_handler = InputHandler()
        input_handler.mouse_wheel_delta = 1
        camera.handle_input(input_handler)
        assert camera.distance == pytest.approx(1.1)

        input_handler.mouse_wheel_delta = -1
        camera.handle_input(input_handler)
        assert camera.distance == pytest.approx(0.9)

        input_handler.mouse_left_held = True
        input_handler.mouse_pos = (10, 20)
        camera.handle_input(input_handler)
        assert camera.azimuth == pytest.approx(10)
        assert camera.elevation == pytest.approx(20)
        
        input_handler.mouse_pos = (12, 22)
        camera.handle_input(input_handler)
        assert camera.azimuth == pytest.approx(12)
        assert camera.elevation == pytest.approx(22)
