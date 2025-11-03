from OpenGL.GL import *
from OpenGL.GLUT import (
    glutInit, glutBitmapCharacter, glutBitmapWidth, GLUT_BITMAP_HELVETICA_18
)

class MainMenu:
    def __init__(self, engine):
        self.engine = engine
        self.button_rect = (540, 300, 200, 80)
        glutInit()

    def update(self, input_handler):
        if input_handler.quit_requested:
            self.engine.running = False
            return

        if input_handler.mouse_pressed:
            x, y = input_handler.mouse_pos
            bx, by, bw, bh = self.button_rect
            if bx <= x <= bx + bw and by <= y <= by + bh:
                self.engine.change_state("simulation")

    def render(self):
        glClearColor(0.0, 0.0, 0.05, 1)
        glLoadIdentity()

        bx, by, bw, bh = self.button_rect
        self.draw_button(bx, by, bw, bh, 0.2, 0.6, 1.0)
        self.draw_text("Universe Simulator", 640, 200, 1.0, 1.0, 1.0, align="center")
        self.draw_text("Start Simulation", bx + bw/2, by + bh/2 + 15, 0.0, 0.0, 0.0, align="center")

    def draw_button(self, x, y, w, h, r, g, b):
        current_color = glGetFloatv(GL_CURRENT_COLOR)
        glColor3f(r, g, b)
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + w, y)
        glVertex2f(x + w, y + h)
        glVertex2f(x, y + h)
        glEnd()
        glColor3f(*current_color[:3])

    def draw_text(self, text, x, y, r, g, b, align="left"):
        current_color = glGetFloatv(GL_CURRENT_COLOR)
        glColor3f(r, g, b)

        width = sum(glutBitmapWidth(GLUT_BITMAP_HELVETICA_18, ord(ch)) for ch in text)

        if align == "center":
            x -= width / 2.0
        elif align == "right":
            x -= width

        glRasterPos2f(x, y)

        for ch in text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

        glColor3f(*current_color[:3])
