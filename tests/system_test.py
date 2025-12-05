"""System tests for the Universe Simulator"""
import pytest
from src import main

@pytest.fixture
def testSystem():
    main.main()