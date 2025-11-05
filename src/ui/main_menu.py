"""Main menu UI module for the Universe Simulator application."""
import OpenGL.GL as gl
import OpenGL.GLUT as glut

class MainMenu:
    """Main menu screen with start button."""
    def __init__(self, engine):
        self.engine = engine
        self.button_rect = (50, 300, 200, 80)

    def update(self, input_handler):
        """Update menu state based on input."""
        if input_handler.quit_requested:
            self.engine.running = False
            return

        if input_handler.mouse_pressed:
            x, y = input_handler.mouse_pos
            bx, by, bw, bh = self.button_rect
            if bx <= x <= bx + bw and by <= y <= by + bh:
                self.engine.change_state("simulation")

    def render(self):
        """Render the main menu."""
        # clear the previous frame
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()

        # switch to orthographic projection
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        gl.glOrtho(0, 1280, 720, 0, -1, 1)  # match window coords
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
        gl.glLoadIdentity()

        # disable depth test so buttons draw on top
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glDisable(gl.GL_LIGHTING)

        # draw the menu
        bx, by, bw, bh = self.button_rect
        self.draw_button(bx, by, bw, bh, 0.2, 0.6, 1.0)
        self.draw_text("Universe Simulator", 150, 200, 1.0, 1.0, 1.0, align="center")
        self.draw_text("Start Simulation", bx + bw/2, by + bh/2 + 15, 0.0, 0.0, 0.0, align="center")

        #draw a few more dummy buttons
        self.draw_button(bx, by+80, bw, bh, 0.2, 0.6, 1.0)
        self.draw_text("dummy button 1", bx + bw/2, by + 80 + bh/2 + 15,
                       0.0, 0.0, 0.0, align="center")
        self.draw_button(bx, by+160, bw, bh, 0.2, 0.6, 1.0)
        self.draw_text("dummy button 2", bx + bw/2, by + 160 + bh/2 + 15,
                       0.0, 0.0, 0.0, align="center")
        self.draw_button(bx, by+240, bw, bh, 0.2, 0.6, 1.0)
        self.draw_text("dummy button 3", bx + bw/2, by + 240 + bh/2 + 15,
                       0.0, 0.0, 0.0, align="center")

        # restore previous GL state
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPopMatrix()
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPopMatrix()

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
        """Draw text at specified position with color and alignment."""
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
