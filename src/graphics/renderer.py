from OpenGL.GL import *
from OpenGL.GLU import *
import math

class Renderer:
    def __init__(self, texture_loader):
        self.texture_loader = texture_loader
        self.planet_textures = {}
        self.initialized = False

    def initialize_textures(self, planet_data):
        if self.initialized:
            return
        for name, texture_path in planet_data.items():
            texture_id = self.texture_loader.load_texture(texture_path)
            self.planet_textures[name] = texture_id
        self.initialized = True

    def setup_lighting(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION,  (0.0, 0.0, 0.0, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE,   (1.0, 1.0, 1.0, 1.0))
        glLightfv(GL_LIGHT0, GL_SPECULAR,  (1.0, 1.0, 1.0, 1.0))
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    def draw_sphere(self, radius, slices=32, stacks=32):
        quad = gluNewQuadric()
        gluQuadricTexture(quad, GL_TRUE)
        gluSphere(quad, radius, slices, stacks)
        gluDeleteQuadric(quad)

    def draw_planet(self, planet):
        name = planet.name.lower()
        if name not in self.planet_textures:
            return

        glPushMatrix()
        glTranslatef(*planet.position)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.planet_textures[name])
        glRotatef(planet.rotation_angle, 0.0, 1.0, 0.0)
        glColor3f(1.0, 1.0, 1.0)
        self.draw_sphere(planet.radius)
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

    def render(self, physics_service, camera):
        """Render all planets from the camera's viewpoint."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # apply dynamic camera
        camera.apply()

        self.setup_lighting()

        for body in physics_service.bodies:
            self.draw_planet(body)
