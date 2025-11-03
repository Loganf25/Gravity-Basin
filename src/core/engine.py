
import pygame
from OpenGL.GL import *
from core.input_handler import InputHandler
from ui.main_menu import MainMenu
from ui.hud import SimulationScreen

class Engine:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((1280, 720), pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption("Universe Simulator")

        self.clock = pygame.time.Clock()
        self.running = True
        self.input_handler = InputHandler()
        self.state = "menu"

        self.main_menu = MainMenu(self)
        self.sim_screen = SimulationScreen(self)

        self.setup_opengl()

    def setup_opengl(self):
        glViewport(0, 0, 1280, 720)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, 1280, 720, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def run(self):
        while self.running:
            self.input_handler.process_events()

            glClear(GL_COLOR_BUFFER_BIT)

            if self.state == "menu":
                self.main_menu.update(self.input_handler)
                self.main_menu.render()
            elif self.state == "simulation":
                self.sim_screen.update(self.input_handler)
                self.sim_screen.render()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def change_state(self, new_state):
        self.state = new_state
