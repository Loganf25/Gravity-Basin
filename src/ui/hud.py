from OpenGL.GL import *
from OpenGL.GLUT import (
    glutInit, glutBitmapCharacter, glutBitmapWidth, GLUT_BITMAP_HELVETICA_18
)

class SimulationScreen:
    def __init__(self, engine):
        self.engine = engine
        self.button_rect = (540, 20, 200, 60)
        glutInit()

    def update(self, input_handler):
        if input_handler.quit_requested:
            self.engine.running = False
            return

        if input_handler.mouse_pressed:
            x, y = input_handler.mouse_pos
            bx, by, bw, bh = self.button_rect
            if bx <= x <= bx + bw and by <= y <= by + bh:
                self.engine.change_state("menu")

    def render(self):
        glClearColor(0.0, 0.0, 0.1, 1)
        glLoadIdentity()

        bx, by, bw, bh = self.button_rect
        self.draw_button(bx, by, bw, bh, 1.0, 0.8, 0.2)
        self.draw_text("Return to Menu", bx + bw/2, by + bh/2 + 10, 0.0, 0.0, 0.0, align="center")
        self.draw_text("Simulation Running...", 640, 350, 0.7, 0.9, 1.0, align="center")

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
