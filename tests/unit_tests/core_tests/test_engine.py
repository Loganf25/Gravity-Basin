import pytest
from src.simulation.models.planet import Planet
from src.core.engine import Engine

class EngineTest:
    @pytest.fixture
    def __init__(self):
        self.engine = Engine()
    
    def testSetupGL(self):
        self.engine.setup_opengl()
    def testPopulateScene(self):
        self.engine.populate_scene()
    def testDeleteSelectedBody(self):
        self.engine.selection_manager.selected_body = Planet("Earth")
        self.engine.delete_selected_body()
    def testRenderUIOverlay(self):
        self.engine.render_ui_overlay()
    def testHandleSimInput(self):
        self.engine.handle_sim_input()
    def testInitializeSimulation(self):
        self.engine.initialize_simulation()
    def testRun(self):
        self.engine.run()
    def testExit(self):
        self.engine.exit()
        
    def runUnitTests(self):
        self.testSetupGL()
        self.testPopulateScene()
        self.testDeleteSelectedBody()
        self.testRenderUIOverlay()
        self.testHandleSimInput()
        self.testInitializeSimulation()
        self.testRun()
        self.testExit()