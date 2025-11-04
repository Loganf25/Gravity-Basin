
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

from core.input_handler import InputHandler
from ui.main_menu import MainMenu
from ui.hud import SimulationScreen
from graphics.renderer import Renderer
from graphics.texture_loader import TextureLoader
from simulation.services.physics_service import PhysicsService
from simulation.data.simulation_data import planet_textures, PLANET_DATA
from simulation.models.planet import Planet
from simulation.models.star import Star
from graphics.camera import Camera

AU_VISUAL_SCALE = 8.0
RADIUS_VISUAL_SCALE = 0.01

class Engine:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((1280, 720), pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption("Universe Simulator")

        self.clock = pygame.time.Clock()
        self.running = True
        self.input_handler = InputHandler()
        self.state = "menu"

        self.physics_service = PhysicsService()
        self.texture_loader = TextureLoader()
        self.renderer = Renderer(self.texture_loader)

        self.camera = Camera()  # dynamic camera instance
        self.textures_initialized = False

        self.main_menu = MainMenu(self)
        self.sim_screen = SimulationScreen(self)

        self.setup_opengl()

    def setup_opengl(self):
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glViewport(0, 0, 1280, 720)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, 1280/720, 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glClearColor(0.0, 0.0, 0.0, 1.0)

    def populate_scene(self):
        """Create Sun and planets, scale for visualization, and register with PhysicsService."""

        for pdata in PLANET_DATA:
            try:
                p = Planet(pdata["name"])
            except Exception:
                class _P: pass
                p = _P()
                p.name = pdata["name"]
                p.mass = pdata["mass"]
                p.texture = pdata["texture"]
                p.color = pdata["color"]
                p.velocity = [0.0, 0.0, 0.0]
                p.rotation_angle = 0.0

            # position along X-axis
            p.position = [pdata["distance_from_sun"] * AU_VISUAL_SCALE, 0.0, 0.0]

            # visual radius
            if pdata["name"].lower() == "sun":
                p.radius = max(1.0, pdata["radius"] * RADIUS_VISUAL_SCALE * 10.0)
            else:
                p.radius = max(0.5, pdata["radius"] * RADIUS_VISUAL_SCALE)

            self.physics_service.register_body(p)





    def render_ui_overlay(self, draw_fn):
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, 1280, 720, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        draw_fn()
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def run(self):
        while self.running:
            self.input_handler.process_events()

            if not self.textures_initialized:
                print("Initializing planet textures...")
                self.texture_loader.initialize_textures(planet_textures)
                self.renderer.initialize_textures(planet_textures)
                self.populate_scene()
                self.textures_initialized = True
                print("Textures and scene populated successfully.")

            if self.state == "menu":
                self.render_ui_overlay(lambda: (self.main_menu.update(self.input_handler),
                                                self.main_menu.render()))
            elif self.state == "simulation":
                self.physics_service.update()
                self.camera.handle_input(self.input_handler)
                self.renderer.render(self.physics_service, self.camera)
                self.render_ui_overlay(lambda: (self.sim_screen.update(self.input_handler),
                                                self.sim_screen.render()))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def change_state(self, new_state):
        if new_state in ["menu", "simulation"]:
            self.state = new_state
