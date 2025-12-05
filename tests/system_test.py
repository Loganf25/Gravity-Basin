"""System tests for the Universe Simulator"""
import pytest
from src.core.engine import Engine
from src.core.states import States

@pytest.fixture
def testSystem():
    engine = Engine()
    engine.setup_opengl()
    engine.initialize_simulation()
    engine.change_state(States.MENU) # menu should now pop-up
    engine.change_state(States.SIMULATION) # simulation should begin
    engine.change_state(States.EXIT) # program should terminate