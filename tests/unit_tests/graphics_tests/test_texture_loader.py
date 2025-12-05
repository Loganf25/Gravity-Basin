import pytest

from src.graphics.texture_loader import TextureLoader

class TestTextureLoader:
    @pytest.fixture
    def __init__(self):
        self.texture_loader = TextureLoader()
        
    def testInitTextures(self):
        self.texture_loader.initialize_textures(None) # should result in FileNotFoundError and IOError
        
    def runUnitTests(self):
        self.testInitTextures()