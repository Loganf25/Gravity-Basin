"""Core engine module for the Universe Simulator application."""
import pygame
import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut

from core.input_handler import InputHandler
from core.selection_manager import SelectionManager
from ui.main_menu import MainMenu
from ui.hud import SimulationScreen
from graphics.renderer import Renderer
from graphics.texture_loader import TextureLoader
from simulation.services.orbit_service import OrbitService
from simulation.services.physics_service import PhysicsService
from simulation.data.simulation_data import planet_textures, PLANET_DATA
from simulation.models.planet import Planet
from simulation.models.star import Star
from graphics.camera import Camera


AU_VISUAL_SCALE = 8.0
RADIUS_VISUAL_SCALE = 0.0001

class Engine:
    """Core engine to run the Universe Simulator application."""
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((1280, 720), pygame.OPENGL | pygame.DOUBLEBUF)
        glut.glutInit()
        pygame.display.set_caption("Universe Simulator")

        self.clock = pygame.time.Clock()
        self.running = True
        self.input_handler = InputHandler()
        self.state = "menu"

        self.physics_service = PhysicsService()
        self.texture_loader = TextureLoader()
        self.orbit_service = OrbitService(self.physics_service)
        self.renderer = Renderer(self.texture_loader)

        self.camera = Camera()  # dynamic camera instance

        self.textures_initialized = False
        self.selection_manager = SelectionManager()
        self.main_menu = MainMenu(self)
        self.sim_screen = SimulationScreen(self)

        self.setup_opengl()

    def setup_opengl(self):
        """Setup basic OpenGL state."""
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDepthFunc(gl.GL_LEQUAL)
        gl.glViewport(0, 0, 1280, 720)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(60, 1280/720, 0.1, 1000.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)

    def populate_scene(self):
        """Create Sun and planets, scale for visualization, and register with PhysicsService."""

        for pdata in PLANET_DATA:
            try:
                p = Planet(pdata["name"])
            except (ValueError, AttributeError):
                class _P: pass
                p = _P()
                p.name = pdata["name"]
                p.mass = pdata["mass"]
                p.texture = pdata["texture"]
                p.color = pdata["color"]
                p.velocity = [0.0, 0.0, 0.0]
                p.rotation_angle = 0.0
                p.initial_position = [0.0, 0.0, 0.0]

            # position along X-axis
            p.position = [pdata["distance_from_sun"] * AU_VISUAL_SCALE, 0.0, 0.0]
            p.initial_position = list(p.position)

            # visual radius
            if pdata["name"].lower() == "sun":
                p.radius = max(1.0, pdata["radius"] * RADIUS_VISUAL_SCALE * 20.0)
            else:
                p.radius = max(0.5, pdata["radius"] * RADIUS_VISUAL_SCALE)

            self.physics_service.register_body(p)

        sun = next((b for b in self.physics_service.bodies if b.name.lower() == "sun"), None)
        if not sun:
            return
        for body in self.physics_service.bodies:
            if body is not sun:
                self.orbit_service.compute_orbit(body, sun)


    def render_ui_overlay(self, draw_fn):
        """Render a UI overlay by switching to orthographic projection."""
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        gl.glOrtho(0, 1280, 720, 0, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glDisable(gl.GL_LIGHTING)
        draw_fn()
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPopMatrix()
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPopMatrix()

    def handle_sim_input(self):
        """Handle input specific to the simulation state."""
        self.camera.handle_input(self.input_handler)

        if self.input_handler.mouse_pressed:
            self.selection_manager.pick_object(self.input_handler.mouse_pos[0],
                                               self.input_handler.mouse_pos[1],
                                               self.physics_service.bodies)
        if self.selection_manager.selected_body:
            #Sets the camera target to the selected body, making it the center
            self.camera.target = self.selection_manager.selected_body.position

    def initialize_simulation(self):
        """Initializes textures and populates the scene."""
        if not self.textures_initialized:
            print("Initializing planet textures...")
            self.texture_loader.initialize_textures(planet_textures)
            self.renderer.initialize_textures(planet_textures)
            self.populate_scene()
            self.textures_initialized = True
            print("Textures and scene populated successfully.")

    def run(self):
        """Main loop of the engine."""
        self.initialize_simulation()
        while self.running:
            self.input_handler.process_events()

            if self.state == "menu":
                self.render_ui_overlay(lambda: (self.main_menu.update(self.input_handler),
                                                self.main_menu.render()))
            elif self.state == "simulation":
                #self.physics_service.update()
                self.handle_sim_input()
                self.renderer.render(self.physics_service, self.camera)
                self.render_ui_overlay(lambda: (self.sim_screen.update(self.input_handler),
                                                self.sim_screen.render()))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def change_state(self, new_state):
        """Change the current state of the engine."""
        if new_state in ["menu", "simulation"]:
            if new_state == "simulation":
                self.physics_service.start()
            self.state = new_state
