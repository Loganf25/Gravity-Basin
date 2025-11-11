"""Main menu UI module for the Universe Simulator application."""
import OpenGL.GL as gl
import OpenGL.GLUT as glut

class MainMenu:
    """Main menu screen with start button."""
    def __init__(self, engine):
        self.engine = engine

        #all the buttons on the hud
        self.button_list = []
        self.button_list.append((50, 300, 200, 80)) # simulation button
        self.button_list.append((50, 400, 200, 80)) # credits button
        self.button_list.append((50, 500, 200, 80)) # quit button

    """is (x,y) within button(bx,by,bw,bh)"""
    def within_bounds(self,x,y,bx,by,bw,bh):
        if bx <= x <= bx + bw and by <= y <= by + bh:
            return True
        return False

    def update(self, input_handler):
        """Update menu state based on input."""
        if input_handler.quit_requested:
            self.engine.running = False
            return

        if input_handler.mouse_pressed:

            x, y = input_handler.mouse_pos

            #for every button
            for i in range(len(self.button_list)):

                bx, by, bw, bh = self.button_list[i]

                #if mouse within some button
                if self.within_bounds(x, y, bx, by, bw, bh):

                    #start simulation button
                    if i == 0:
                        self.engine.change_state("simulation")
                    if i == 1:
                        #self.engine.change_state("credits") will be implemented
                        print("sorry non functional right now, credits screen doesent exist yet")
                        break
                    if i == 2:
                        #self.exit program (whatever the proper function for this is)
                        print("nope you get to stay forever")
                        break

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

        # draw the title
        self.draw_text("Universe Simulator", 400, 200, 1.0, 1.0, 1.0, align="center", scale = 120)

        #draw each button in button list
        for i in range(len(self.button_list)):
            bx, by, bw, bh = self.button_list[i]

            if i == 0:
                self.draw_button(bx, by, bw, bh, 0.2, 0.6, 1.0)
                self.draw_text("Start Simulation", bx + bw/2, by + bh/2 + 15, 0.0, 0.0, 0.0, align="center")
            if i == 1:
                self.draw_button(bx, by, bw, bh, 0.2, 0.6, 1.0)
                self.draw_text("Credits", bx + bw/2, by + bh/2 + 15, 0.0, 0.0, 0.0, align="center")
            if i == 2:
                self.draw_button(bx, by, bw, bh, 1,0,0)
                self.draw_text("Exit", bx + bw/2, by + bh/2 + 15, 0.0, 0.0, 0.0, align="center")

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

    def draw_text(self, text, x, y, r, g, b, align="left", scale=40):

        """scaled text"""
        if scale != 40:

            """Draw scalable text using GLUT stroke fonts."""
            current_color = gl.glGetFloatv(gl.GL_CURRENT_COLOR)
            gl.glColor3f(r, g, b)

            gl.glPushMatrix()
            gl.glTranslatef(x, y, 0.0)
            gl.glScalef(scale * 0.005, scale * -0.005, 1.0)  # scale visual size

            # approximate width for alignment
            width = sum(glut.glutStrokeWidth(glut.GLUT_STROKE_ROMAN, ord(ch)) for ch in text)

            if align == "center":
                gl.glTranslatef(-width / 2.0, 0.0, 0.0)
            elif align == "right":
                gl.glTranslatef(-width, 0.0, 0.0)

            for ch in text:
                glut.glutStrokeCharacter(glut.GLUT_STROKE_ROMAN, ord(ch))

            gl.glPopMatrix()
            gl.glColor3f(*current_color[:3])

        
        else:
            """non scaled text"""
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