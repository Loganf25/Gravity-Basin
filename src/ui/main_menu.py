from OpenGL.GL import *
from OpenGL.GLUT import (
    glutInit, glutBitmapCharacter, glutBitmapWidth, GLUT_BITMAP_HELVETICA_18
)

class MainMenu:
    def __init__(self, engine):
        self.engine = engine
        self.button_rect = (50, 300, 200, 80)
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
        # clear the previous frame
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # switch to orthographic projection
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, 1280, 720, 0, -1, 1)  # match window coords
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # disable depth test so buttons draw on top
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)

        # draw the menu
        bx, by, bw, bh = self.button_rect
        self.draw_button(bx, by, bw, bh, 0.2, 0.6, 1.0)
        self.draw_text("Universe Simulator", 150, 200, 1.0, 1.0, 1.0, align="center")
        self.draw_text("Start Simulation", bx + bw/2, by + bh/2 + 15, 0.0, 0.0, 0.0, align="center")

        #draw a few more dummy buttons
        self.draw_button(bx, by+80, bw, bh, 0.2, 0.6, 1.0)
        self.draw_text("dummy button 1", bx + bw/2, by + 80 + bh/2 + 15, 0.0, 0.0, 0.0, align="center")
        self.draw_button(bx, by+160, bw, bh, 0.2, 0.6, 1.0)
        self.draw_text("dummy button 2", bx + bw/2, by + 160 + bh/2 + 15, 0.0, 0.0, 0.0, align="center")
        self.draw_button(bx, by+240, bw, bh, 0.2, 0.6, 1.0)
        self.draw_text("dummy button 3", bx + bw/2, by + 240 + bh/2 + 15, 0.0, 0.0, 0.0, align="center")

        # restore previous GL state
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

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
