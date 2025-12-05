import pytest
from src.core.engine import Engine

class EngineTest:
    @pytest.fixture
    def test_engine(self, engine):
        engine.run()
        assert engine.running is True
