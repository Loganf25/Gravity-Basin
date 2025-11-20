"""Unit Tests for the Time Manager Module"""
import pytest
from src.core.time_manager import TimeManager

class TestTimeManager:
    """Tests for the TimeManager class
        Unit tests should tests just single units,
        doesn't neccessaryly have to be each function,
        but what may happen when they are used together as well."""

    @pytest.fixture
    def time_manager(self):
        """Create a TimeManager for tests
        Don't want to reuse the same one across tests
        And this is cleaner than a new timemanager
        object per test function"""
        return TimeManager()

    def test_initial_state(self, time_manager):
        """Test initial state of TimeManager"""
        assert time_manager.paused is True
        assert time_manager.sim_scale == 0.0
        assert time_manager.base_time_scale == 3e6
        assert time_manager.time_multiplier == 1.0

    