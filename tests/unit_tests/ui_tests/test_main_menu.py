import pytest

from src.core.engine import Engine
from src.core.engine import InputHandler
from src.ui.main_menu import button
from src.ui.main_menu import MainMenu

class TestMainMenu():
    @pytest.fixture
    def __init__(self):
        self.engine = Engine()
        self.main_menu = MainMenu(self.engine)

        
    def testInit(self):
        assert self.main_menu.engine == self.engine
    def testWithinBounds(self):
        assert self.main_menu.within_bounds(x=0, y=0, button=button(bx=0,by=0,bw=0,bh=0)) == True
    def testUpdate(self):
        input_handler = InputHandler()
        input_handler.quit_requested = True
        self.main_menu.update(input_handler) # Should make main menu engine no longer running
        assert self.main_menu.engine.running == False
    def testRender(self):
        self.main_menu.render() # Renders main menu
    def testDrawButton(self):
        self.main_menu.draw_button(button(bx=150,by=150,bw=150,bh=150), 0,0,0) # Draws a white button
    def testDrawText(self):
        self.main_menu.draw_text("Test", x=50, y=50)
    def testDrawCredits(self):
        self.main_menu.draw_credits()
    def testDrawImage(self):
        self.main_menu.draw_image("assests/Earth.png", x=50, y=50, width=200, height=200)
    
    def runUnitTests(self):
        self.testInit()
        self.testWithinBounds()
        self.testUpdate()
        self.testRender()
        self.testDrawButton()
        self.testDrawText()
        self.testDrawCredits()
        self.testDrawImage()