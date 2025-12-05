import pytest
from src.core.selection_manager import SelectionManager

class test_selection_manager:
    def __init__(self):
        self.selection_manager = SelectionManager()
        
    @pytest.fixture
    def test_selection_manager(self):
        assert self.selection_manager.get_selected_body() == None
        
    def runUnitTests(self):
        self.test_selection_manager()