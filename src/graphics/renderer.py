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

    def draw_orbit(self, trail):
        """Draw the orbit path from a list of points with a fading red effect."""
        if len(trail) < 2:
            return

        gl.glDisable(gl.GL_LIGHTING)
        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        # Draw the fading line strip
        gl.glLineWidth(2.0)
        gl.glBegin(gl.GL_LINE_STRIP)
        num_points = len(trail)
        #Create fading effect
        for i, point in enumerate(trail):
            # Alpha fades from 0 (transparent) to 1 (opaque blue) along the trail
            alpha = (i / (num_points - 1)) ** 2
            gl.glColor4f(0.227, 0.298, 0.478, alpha) # Fading blue color
            gl.glVertex3fv(point)
        gl.glEnd()

        # Draw a rounded point at the head of the trail
        gl.glEnable(gl.GL_POINT_SMOOTH)
        gl.glPointSize(3.0)
        gl.glBegin(gl.GL_POINTS)
        gl.glColor4f(0.227, 0.298, 0.478, 1.0)
        gl.glVertex3fv(trail[-1])
        gl.glEnd()
        gl.glDisable(gl.GL_POINT_SMOOTH)

        gl.glDisable(gl.GL_BLEND)

    def render(self, physics_service, camera):
        """Render all planets from the camera's viewpoint."""
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()

        # apply dynamic camera
        camera.apply()

        for body in physics_service.bodies:
            if hasattr(body, 'trail') and body.name.lower() != "sun":
                self.draw_orbit(body.trail)

        self.setup_lighting()

        for body in physics_service.bodies:
            self.draw_planet(body)
