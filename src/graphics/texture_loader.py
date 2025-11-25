""""module for loading and managing textures using OpenGL and Pygame"""
import os
import ctypes
import pygame
import OpenGL.GL as gl

class TextureLoader:
    """Loads and manages textures using OpenGL and Pygame"""
    def __init__(self):
        self.textures = {}
        self.textures_loaded = False

    def load_texture(self, file_path):

        #get relative path and graft it onto abosolute path to create a robust pathing
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_dir, file_path)

        """Load a texture from file and return its OpenGL texture ID"""
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

        texture_id = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)

        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

        gl_format = gl.GL_RGBA if image_format == "RGBA" else gl.GL_RGB
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl_format,
                        width, height, 0, gl_format, gl.GL_UNSIGNED_BYTE, buf)

        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        self.textures[file_path] = texture_id
        return texture_id

    def initialize_textures(self, planet_textures):
        """Loads all planet textures and stores their OpenGL IDs"""
        try:
            for planet, path in planet_textures.items():
                tex_id = self.load_texture(path)
                print(f"Loaded {planet}: {path} (ID={tex_id})")
        except (FileNotFoundError, IOError) as e:
            print(f"Failed to load {planet} texture: {e}")
        else:
            print("All textures initialized successfully.")
            self.textures_loaded = True
            
