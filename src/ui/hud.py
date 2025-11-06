"""Simulation HUD module for the Universe Simulator application."""
import OpenGL.GL as gl
import OpenGL.GLUT as glut

class SimulationScreen:
    """Heads-up display for the simulation screen with return to menu button."""
    def __init__(self, engine):
        self.engine = engine

        #all the buttons on the hud
        self.button_list = []
        self.button_list.append((50, 80, 150, 50)) # back button

        #build the time controls buttons
        #todo
        self.button_list.append((50, 10, 250, 50)) #temp button (false button)
        #build the planet controls buttons
        #todo
        self.button_list.append((50, 600, 700, 70)) #temp button (false button)
        #build the object menu buttons
        #todo
        self.button_list.append((1000, 10, 260, 700)) #temp button (false button)

        #building the planet adding buttons
        for i in range(12):
            if i % 2 == 0:
                self.button_list.append((1000+20, 33+i*55, 100, 100))
                self.button_list.append((1000+140, 33+i*55, 100, 100))


    """is (x,y) within button(bx,by,bw,bh)"""
    def within_bounds(self,x,y,bx,by,bw,bh):
        if bx <= x <= bx + bw and by <= y <= by + bh:
            return True
        return False

    def update(self, input_handler):
        """Update HUD state based on input."""
        if input_handler.quit_requested:
            self.engine.running = False
            return

        """if mouse if pressed, check button hitbox collisions"""
        if input_handler.mouse_pressed:

            x, y = input_handler.mouse_pos

            #for every button
            for i in range(len(self.button_list)):

                bx, by, bw, bh = self.button_list[i]

                #if mouse within some button
                if self.within_bounds(x, y, bx, by, bw, bh):

                    #back to menu button
                    if i == 0:
                        self.engine.change_state("menu")

                    #all three are debug buttons, they will still render but will actually be ignored
                    #time controls buttons
                    if i == 1:
                        print("clicking time controls box")

                    #planet controls buttons
                    if i == 2:
                        print("planet controls box")

                    #object menu buttons
                    if i == 3:
                        print("object menu box")

                    #time controls will have a few buttons (pause/play reverse, double speed, half speed)
                    
                    #planet controls (will either be entirely informational or allows for modifcation of 
                    # planet attributes (mass,radius,volume) in a way reminacient of changing magnitudes 
                    # (so will be doublings and halvings but no input boxes [too complex]))

                    #object menu 1 button for each planet

    def render(self):
        """Render the simulation HUD."""
        gl.glClearColor(0.0, 0.0, 0.1, 1)
        gl.glLoadIdentity()

        #draw each button in button list
        for i in range(len(self.button_list)):
            bx, by, bw, bh = self.button_list[i]

            if i == 0:
                #place in back to menu button
                self.draw_button(bx, by, bw, bh, 1,0,0)
                self.draw_text("Return to Menu", bx + bw/2, by + bh/2 + 10, 0.0, 0.0, 0.0, align="center")
            if i > 0:
                #place in rects for each ui element zone, with white trim
                self.draw_trimmed_button(bx, by, bw, bh, 0, 0, 0, 1, 1, 1)

    def draw_trimmed_button(self, x, y, w, h, r, g, b, tr, tg, tb):
        """draw a button with some trim to it"""
        self.draw_button(x-1,y-1,w+2,h+2, tr,tg,tb) #colored trim
        self.draw_button(x,y,w,h, r,g,b)    #main rect
        
    
    def draw_button_text(self, text, x, y, w, h, r, g, b):
        """Draw a button with text."""
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
