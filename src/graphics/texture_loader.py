
from OpenGL.GL import *
import pygame
import ctypes
import os

class TextureLoader:
    def __init__(self):
        self.textures = {}

    def load_texture(self, file_path):
        if file_path in self.textures:
            return self.textures[file_path]

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Texture not found: {file_path}")

        surface = pygame.image.load(file_path)
        surface = pygame.transform.flip(surface, False, True)

        image_format = "RGBA" if surface.get_bytesize() == 4 else "RGB"
        image_data = pygame.image.tostring(surface, image_format, True)
        width, height = surface.get_size()

        #safe contiguous buffer for OpenGL
        buf = (ctypes.c_ubyte * len(image_data)).from_buffer_copy(image_data)

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        gl_format = GL_RGBA if image_format == "RGBA" else GL_RGB
        glTexImage2D(GL_TEXTURE_2D, 0, gl_format, width, height, 0, gl_format, GL_UNSIGNED_BYTE, buf)

        glBindTexture(GL_TEXTURE_2D, 0)
        self.textures[file_path] = texture_id
        return texture_id

    def initialize_textures(self, planet_textures):
        """Loads all planet textures and stores their OpenGL IDs"""
        print("Initializing planet textures...")
        for planet, path in planet_textures.items():
            try:
                tex_id = self.load_texture(path)
                print(f"Loaded {planet}: {path} (ID={tex_id})")
            except Exception as e:
                print(f"Failed to load {planet} texture: {e}")
        print("All textures initialized successfully.")
