"""Simulation HUD module for the Universe Simulator application."""
import OpenGL.GL as gl
import OpenGL.GLUT as glut

class SimulationScreen:
    """Heads-up display for the simulation screen with return to menu button."""
    def __init__(self, engine):
        self.engine = engine
<<<<<<< HEAD
        self.button_rect = (540, 20, 200, 60)
=======
        self.button_rect = (50, 80, 160, 50)
        glutInit()
>>>>>>> bf9c5fffab07fe02644c4d29abbcd9a5866c1c99

    def update(self, input_handler):
        """Update HUD state based on input."""
        if input_handler.quit_requested:
            self.engine.running = False
            return

        if input_handler.mouse_pressed:
            x, y = input_handler.mouse_pos
            bx, by, bw, bh = self.button_rect
            if bx <= x <= bx + bw and by <= y <= by + bh:
                self.engine.change_state("menu")

    def render(self):
        """Render the simulation HUD."""
        gl.glClearColor(0.0, 0.0, 0.1, 1)
        gl.glLoadIdentity()

        bx, by, bw, bh = self.button_rect
        self.draw_button(bx, by, bw, bh, 1.0, 0.8, 0.2)
        self.draw_text("Return to Menu", bx + bw/2, by + bh/2 + 10, 0.0, 0.0, 0.0, align="center")

        #place in ui elements approximate positions
        self.draw_button_text("[time controls]",50, 10, 250, 50, 1.0, 0.8, 0.2)
        self.draw_button_text("[planet controls]",50, 600, 700, 70, 1.0, 0.8, 0.2)
        self.draw_button_text("[object menu]",1000, 10, 260, 700, 1.0, 0.8, 0.2)

    def draw_button_text(self, text, x, y, w, h, r, g, b):
        self.draw_button(x,y,w,h, r,g,b)
        self.draw_text(text, x + w/2, y + h/2 + 10, 0,0,0, align="center")


    def draw_button(self, x, y, w, h, r, g, b):
        """Draw a colored rectangle button."""
        current_color = gl.glGetFloatv(gl.GL_CURRENT_COLOR)
        gl.glColor3f(r, g, b)
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex2f(x, y)
        gl.glVertex2f(x + w, y)
        gl.glVertex2f(x + w, y + h)
        gl.glVertex2f(x, y + h)
        gl.glEnd()
        gl.glColor3f(*current_color[:3])

    def draw_text(self, text, x, y, r, g, b, align="left"):
        """Draw text at specified position with alignment."""
        current_color = gl.glGetFloatv(gl.GL_CURRENT_COLOR)
        gl.glColor3f(r, g, b)

        width = sum(glut.glutBitmapWidth(glut.GLUT_BITMAP_HELVETICA_18, ord(ch)) for ch in text)

        if align == "center":
            x -= width / 2.0
        elif align == "right":
            x -= width

        gl.glRasterPos2f(x, y)

        for ch in text:
            glut.glutBitmapCharacter(glut.GLUT_BITMAP_HELVETICA_18, ord(ch))

        gl.glColor3f(*current_color[:3])
