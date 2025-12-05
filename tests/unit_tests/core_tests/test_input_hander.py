import pytest
from src.core.input_handler import InputHandler

class testInputHandler:
    def __init__(self):
        self.input_handler = InputHandler()
    
    @pytest.fixture
    def test_input_handler(self):
        self.input_handler.process_events()
        assert self.input_handler.last_mouse_pos != None