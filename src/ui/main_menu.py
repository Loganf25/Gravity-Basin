"""Main menu UI module for the Universe Simulator application."""
import OpenGL.GL as gl
import OpenGL.GLUT as glut
from core.states import States
from graphics.texture_loader import TextureLoader

class button:
    def __init__(self, bx, by,  bw, bh):
        self.bx = bx
        self.by = by
        self.bw = bw
        self.bh = bh

class MainMenu:
    """Main menu screen with start button."""
    def __init__(self, engine):
        self.engine = engine

        #all the buttons on the hud
        self.button_list = {}
        bx, by, bw, bh = 50, 300, 200, 80
        self.button_list[States.SIMULATION] = button(bx, by, bw, bh) # simulation button
        by += 100
        self.button_list[States.CREDITS] = button(bx, by, bw, bh) # credits button
        by += 100
        self.button_list[States.EXIT] = button(bx, by, bw, bh) # quit button

    """is (x,y) within button(bx,by,bw,bh)"""
    def within_bounds(self,x,y,button):
        if ((button.bx <= x <= button.bx + button.bw) and (button.by <= y <= button.by + button.bh)):
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
            for button_key in self.button_list:

                button_obj = self.button_list[button_key]

                #if mouse within some button
                if self.within_bounds(x, y, button_obj):

                    #start simulation button
                    if button_key is States.SIMULATION:
                        self.engine.change_state(States.SIMULATION)
                    if button_key is States.CREDITS:
                        self.engine.change_state(States.CREDITS)
                        break
                    if button_key is States.EXIT:
                        #self.exit program (whatever the proper function for this is)
                        self.engine.change_state(States.EXIT)
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
        for button_key in self.button_list:
            button_obj = self.button_list[button_key]
            x = button_obj.bx + button_obj.bw/2
            y = button_obj.by + button_obj.bh/2 + 15
            
            if button_key is States.SIMULATION:
                self.draw_button(button_obj, 0.2, 0.6, 1.0)
                self.draw_text("Start Simulation", x, y, 0.0, 0.0, 0.0, align="center")
            if button_key is States.CREDITS:
                self.draw_button(button_obj, 0.2, 0.6, 1.0)
                self.draw_text("Credits", x, y, 0.0, 0.0, 0.0, align="center")
            if button_key is States.EXIT:
                self.draw_button(button_obj, 1,0,0)
                self.draw_text("Exit", x, y, 0.0, 0.0, 0.0, align="center")

        # restore previous GL state
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPopMatrix()
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPopMatrix()

    def draw_button(self, button_obj, r, g, b):
        """Draw a colored rectangle button."""
        current_color = gl.glGetFloatv(gl.GL_CURRENT_COLOR)
        gl.glColor3f(r, g, b)
        gl.glBegin(gl.GL_QUADS)
        x, y, w, h = button_obj.bx, button_obj.by, button_obj.bw, button_obj.bh
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

    def draw_text(self, text, x, y, r=1.0, g=1.0, b=1.0, align="left", scale=40):

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
                
                
    def __update_xy(self, y, mult = 1):
        PADDING = 50
        update = (lambda y, padding: y+padding)
        y = update(y, PADDING * mult)
        
        return (y)

    def draw_credits(self):
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
        
        tl = TextureLoader()
        star_id = tl.load_texture("assets/images/stars.jpg")

        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glBindTexture(gl.GL_TEXTURE_2D, star_id)
        # draw quad the size of the screen to make backgroud image
        gl.glBegin(gl.GL_QUADS)
        gl.glTexCoord2f(0, 0); gl.glVertex2f(0, 0)
        gl.glTexCoord2f(1, 0); gl.glVertex2f(1280, 0)
        gl.glTexCoord2f(1, 1); gl.glVertex2f(1280, 720)
        gl.glTexCoord2f(0, 1); gl.glVertex2f(0, 720)
        gl.glEnd()
        gl.glDisable(gl.GL_TEXTURE_2D)

        # draw credits
        x = 300
        y = 100
        self.draw_text("CREDITS", x, y, align="center", scale = 120); y = self.__update_xy(y)
        self.draw_text("TEAM LEAD", x,y); y = self.__update_xy(y)
        self.draw_text("----------", x,y); y = self.__update_xy(y)
        self.draw_text("MILES", x,y); y = self.__update_xy(y, mult=2)
        self.draw_text("CODING", x,y); y = self.__update_xy(y)
        self.draw_text("--------", x,y); y = self.__update_xy(y)
        self.draw_text("CASSANDRA LEDER", x,y); y = self.__update_xy(y)
        self.draw_text("LOGAN", x,y)
        
        # restore previous GL state
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPopMatrix()
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPopMatrix()

