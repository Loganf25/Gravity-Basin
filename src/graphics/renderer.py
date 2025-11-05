"""module for rendering planets using OpenGL"""
import math
import OpenGL.GL as gl
import OpenGL.GLU as glu

class Renderer:
    """Renders planets using OpenGL with textures."""
    def __init__(self, texture_loader):
        self.texture_loader = texture_loader
        self.planet_textures = {}
        self.initialized = False

    def initialize_textures(self, planet_data):
        """Load all planet textures using the provided texture loader."""
        if self.initialized:
            return
        for name, texture_path in planet_data.items():
            texture_id = self.texture_loader.load_texture(texture_path)
            self.planet_textures[name] = texture_id
        self.initialized = True

    def setup_lighting(self):
        """Setup basic lighting for the scene."""
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION,  (0.0, 0.0, 0.0, 1.0))
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE,   (1.0, 1.0, 1.0, 1.0))
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_SPECULAR,  (1.0, 1.0, 1.0, 1.0))
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glColorMaterial(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE)

    def draw_sphere(self, radius, slices=32, stacks=32):
        """Draw a textured sphere."""
        quad = glu.gluNewQuadric()
        glu.gluQuadricTexture(quad, gl.GL_TRUE)
        glu.gluSphere(quad, radius, slices, stacks)
        glu.gluDeleteQuadric(quad)

    def draw_planet(self, planet):
        """Draw a planet with its texture."""
        name = planet.name.lower()

        gl.glPushMatrix()
        gl.glTranslatef(*planet.position)
        gl.glRotatef(planet.rotation_angle, 0.0, 1.0, 0.0)
        #Sun 
        if name == "sun":
            gl.glDisable(gl.GL_LIGHTING)
            gl.glColor3f(1.0, 1.0, 1.0)
            self.draw_sphere(planet.radius)
            gl.glEnable(gl.GL_LIGHTING)
        #Pre defined planets 
        elif name in self.planet_textures:
            gl.glEnable(gl.GL_TEXTURE_2D)
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.planet_textures[name])
            gl.glColor3f(1.0, 1.0, 1.0)
            self.draw_sphere(planet.radius)
            gl.glDisable(gl.GL_TEXTURE_2D)
        else:
            #Fallback for custom planets without textures
            self.draw_sphere(planet.radius)
        gl.glPopMatrix()

    def draw_orbit(self, radius):
        """Draw the orbit path as a circle in the XZ plane."""
        gl.glDisable(gl.GL_LIGHTING)
        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glColor3f(0.3, 0.3, 0.3)
        gl.glBegin(gl.GL_LINE_LOOP)

        num_segments = 100
        for i in range(num_segments):
            angle = 2 * math.pi * i / num_segments
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            gl.glVertex3f(x, 0.0, z)

        gl.glEnd()

    def render(self, physics_service, camera):
        """Render all planets from the camera's viewpoint."""
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()

        # apply dynamic camera
        camera.apply()

        for body in physics_service.bodies:
            if body.name.lower() != "sun":
                dist = math.sqrt(body.initial_position[0]**2 + body.initial_position[1]**2 + body.initial_position[2]**2)
                self.draw_orbit(dist)

        self.setup_lighting()

        for body in physics_service.bodies:
            self.draw_planet(body)
