import pytest
from src.core.engine import Engine
from src.ui.hud import SimulationScreen
from src.simulation.models.celestial_body import CelestialBody
from src.core.input_handler import InputHandler

class testSimulationScreen:
    @pytest.fixture
    def __init__(self):
        self.engine = Engine()
        self.hud = SimulationScreen(self.engine)
        
    def testInit(self):
        assert len(self.hud.button_list) > 0
        assert len(self.hud.label) > 0
    def testUpdateLabel(self):
        assert self.hud.label[0] != "Null"
        self.hud.update_label("Null", 0)
        assert self.hud.label[0] == "Null"
    def testRecalculateLabel(self):
        self.hud.engine.selection_manager.current_body = CelestialBody("Null", 0, 0, 0, None, None, None)
        self.hud.recalculate_labels() # label should now be all 0s
    def testWithinBounds(self):
        assert self.hud.within_bounds(x=0,y=0,bx=0,by=0,bw=0,bh=0) == True
    def testUpdate(self):
        input_handler = InputHandler()
        input_handler.quit_requested = True
        self.hud.update(input_handler)
        assert self.hud.engine.running == False
    def testRenderer(self):
        self.hud.render()
    def testDrawTrimmedButton(self):
        self.hud.draw_trimmed_button(x=50,y=50,w=200,h=200,r=0,g=0,b=0,tr=0,tg=0,tb=0)
    def testDrawButtonText(self):
        self.testDrawButtonText()
        self.hud.draw_button_text("Button", 50, 50, 100, 100, 0,0,0)
    def testDrawButton(self):
        self.hud.draw_button(x=50,y=50,w=200,h=200, r=0,g=0,b=0)
    def testDrawText(self):
        self.hud.draw_text("Test", x=50, y=50, r=0, g=0, b=0)
   