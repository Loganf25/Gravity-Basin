"""Simulation HUD module for the Universe Simulator application."""
import OpenGL.GL as gl
import OpenGL.GLUT as glut
from simulation.data.simulation_data import planet_textures, PLANET_DATA
from simulation.services.physics_service import PhysicsService
from core.states import States

class SimulationScreen:
    """Heads-up display for the simulation screen with return to menu button."""
    def __init__(self, engine):
        self.engine = engine

        #all the buttons on the hud
        self.button_list = []
        self.label = []
        self.locked = 0

        self.button_list.append((50, 80, 140, 50)) # back button 0

        #the 3 button regions
        self.button_list.append((50, 10, 140, 50)) # time controls box (false button) 1 
        self.button_list.append((50, 500, 570, 210)) # planet info box (false button) 2
        self.button_list.append((1000, 10, 260, 700)) # object menu box (false button) 3

        #building the planet adding buttons
        for index in range(12):
            if index % 2 == 0:
                self.button_list.append((1000+20, 33+index*55, 100, 100))
                self.button_list.append((1000+140, 33+index*55, 100, 100))

        # real time buttons (id 16-18)
        self.button_list.append((55, 15, 40, 40)) # half time speed 16
        self.button_list.append((100, 15, 40, 40)) # pause / play time 17
        self.button_list.append((145, 15, 40, 40)) # double time speed 18

        # planet info buttons (19-28)
        self.button_list.append((60, 560, 40, 40)) # mass half 19
        self.button_list.append((60, 610, 40, 40)) # volume half 20
        self.button_list.append((60, 660, 40, 40)) # density half 21
        self.button_list.append((110, 560, 40, 40)) # mass double 22
        self.button_list.append((110, 610, 40, 40)) # volume double 23
        self.button_list.append((110, 660, 40, 40)) # density double 24
        self.button_list.append((160, 560, 40, 40)) # mass lock 25
        self.button_list.append((160, 610, 40, 40)) # volume lock 26
        self.button_list.append((160, 660, 40, 40)) # density lock 27

        self.button_list.append((410, 510, 200, 40)) # delete planet button 28

        self.button_list.append((200, 80, 140, 50)) # reset simulation 29

        #labels (gets updated during runtime)
        self.label.append("[update time speed here]") # current time speed 0
        self.label.append("[update mass speed here]") # current mass 1
        self.label.append("[update volume speed here]") # current volume 2
        self.label.append("[update density speed here]") # current density 3
        self.label.append("[update planet name here]") # current object name 4

    """simple function to update the labels (used in engine, or gets values from engine and updates within hud)"""
    def update_label(self, text, i):

        """Update label text at index i.
         Inputs:
            text: New text for the label
            i: Index of the label to update
        Outputs:
            None
        """
        self.label[i] = text

    """simple function to update label text field based on currently selected object"""
    def recalculate_labels(self):
        planet = self.engine.selection_manager.get_selected_body()
        
        if planet is not None:
            self.update_label(str(planet.get_mass()),1)
            self.update_label(str(planet.get_volume()),2)
            self.update_label(str(planet.get_density()),3)
            self.update_label(str(planet.get_name()),4)

    """is (x,y) within button(bx,by,bw,bh)"""
    def within_bounds(self,x,y,bx,by,bw,bh):
        """Is x,y position withing rectangle bounds bx,by,bw,bh?

            Inputs
                x - x position
                
                y - y position
                bx - box x position
                by - box y position
                bw - box width
                bx - box height
            Outputs
                boolean True/False
        """
        if bx <= x <= bx + bw and by <= y <= by + bh:
            return True
        return False

    """function is the button input handler and activates specific functions for specific button id's hit"""
    def update(self, input_handler):

        """Update HUD state based on input."""
        if input_handler.quit_requested:
            self.engine.running = False
            return

        """if mouse if pressed, check button hitbox collisions"""
        if input_handler.mouse_pressed:

            x, y = input_handler.mouse_pos
            self.recalculate_labels()

            #for every button
            for button_index in range(len(self.button_list)):

                bx, by, bw, bh = self.button_list[button_index]

                #if mouse within some button
                if self.within_bounds(x, y, bx, by, bw, bh):

                    match button_index:
                        
                        case 0:
                            self.engine.change_state(States.MENU)   #menu button
                        case 16:
                            self.engine.time_manager.decrease_speed()   # /2 time button
                        case 17:
                            self.engine.time_manager.toggle_pause()     # play/pause time button
                        case 18:
                            self.engine.time_manager.increase_speed()   # *2 time button
                        case 25:    #mass lock
                            if self.locked == 1:
                                self.locked = 0
                            else:
                                self.locked = 1                            
                        case 26:    #volume lock
                            if self.locked == 2:
                                self.locked = 0
                            else:
                                self.locked = 2
                        case 27:    #density lock
                            if self.locked == 3:
                                self.locked = 0
                            else:
                                self.locked = 3
                    
                        #planet info modifier buttons
                        case 19 | 20 | 21 | 22 | 23 | 24:

                            if button_index >= 19 and button_index <= 21:
                                modifier = 0.5
                            else:
                                modifier = 2.0
                            planet = self.engine.selection_manager.get_selected_body()

                            #encodes which attribute is being targeted
                            match button_index:
                                case 19 | 22:
                                    attribute = 0
                                case 20 | 23:
                                    attribute = 1
                                case 21 | 24:
                                    attribute = 2

                            #calculate the result of modifying that attribute
                            planet.recalculate(self.locked, modifier, attribute)

                            #label update
                            self.recalculate_labels()

                        case 28: #delete planet button
                            self.engine.delete_selected_body()
                        case 29: #reset planet button
                            self.engine.populate_scene()

                        #object adding buttons
                        case _ if 4 <= button_index <= 15:
                            self.engine.populate_scene(button_index - 4)   

    """function draws visual hud graphics to screen (button visuals / text)"""
    def render(self):

        """Render the simulation HUD."""
        gl.glClearColor(0.0, 0.0, 0.1, 1)
        gl.glLoadIdentity()

        #draw each button in button list
        for button_index in range(len(self.button_list)):
            bx, by, bw, bh = self.button_list[button_index]


            text = None
            button_color = [0,0,0]
            text_color = [1,1,1]
            trim_color = [1,1,1]
            attribute_test = ["Mass","Volume","Density"]
            
            #defining custom colors for buttons
            match button_index:
                case 0:
                    text_color = [0,0,0]
                    trim_color = [0,0,0]
                    button_color = [1,0,0]
                case 28:
                    text_color = [0,0,0]
                    trim_color = [0,0,0]
                    button_color = [1,0,0]

            self.draw_trimmed_button(bx, by, bw, bh, button_color[0], button_color[1], button_color[2], trim_color[0], trim_color[1], trim_color[2])


            match button_index:
                
                #menu button
                case 0:
                    text = "Return to Menu"

                # divider: /2
                case 16 | 19 | 20 | 21:
                    text = "/2"

                # start/pause
                case 17:
                    text = "s/p"
                    self.draw_text("current time : " + self.label[button_index-17],bx + bw/2 + 85, by + bh/2 + 10,1, 1, 1, align="left")

                # multiplier: *2
                case 18 | 22 | 23 | 24:
                    text = "*2"

                # lock buttons and planet info labels
                case 25 | 26 | 27:

                    # label
                    self.draw_text("current "+attribute_test[button_index-25]+" : " + self.label[button_index-24],bx + bw/2 + 45, by + bh/2 + 10,1, 1, 1, align="left")

                    # checkbox text
                    lock_id = button_index - 24
                    text = "[X]" if self.locked == lock_id else "[ ]"

                # delete planet button and object name label
                case 28:
                    text = "Delete selected object"
                    self.draw_text("current object : " + self.label[button_index-24],bx + bw/2 -450, by + bh/2 + 10,1, 1, 1, align="left")
                case 29:
                    text = "Reset scene"

                case _:
                    text = None

            #actually draws the text defined in the match cases
            if text:
                self.draw_text(text,bx + bw/2,by + bh/2 + 10,text_color[0], text_color[1], text_color[2],align="center")
            
            

    """draw a button with some trim to it"""
    def draw_trimmed_button(self, x, y, w, h, r, g, b, tr, tg, tb):
        """
            inputs
                x,y - x,y horizontal/vertical displacement respecfully of the button with trim in pixels from top left corner of screen
                w,h - width and height of rectangle in pixels
                rgb - colors of rectangle in rgb format [0,1]
                tr,tg,tb - trim's rgb values
            output
                Draw a colored rectangle with white text
        """

        self.draw_button(x-1,y-1,w+2,h+2, tr,tg,tb) #colored trim
        self.draw_button(x,y,w,h, r,g,b)            #main rect
        
    """draw a button with text"""
    def draw_button_text(self, text, x, y, w, h, r, g, b):

        """
            inputs
                text - string input
                x,y - x,y horizontal/vertical displacement respecfully of the button with text in pixels from top left corner of screen
                w,h - width and height of rectangle in pixels
                rgb - colors of rectangle in rgb format [0,1]
            output
                Draw a colored rectangle with white text
        """

        self.draw_button(x,y,w,h, r,g,b)
        self.draw_text(text, x + w/2, y + h/2 + 10, 0,0,0, align="center")

    """draw a rectangle on screen"""
    def draw_button(self, x, y, w, h, r, g, b):

        """
            inputs
                x,y - x,y horizontal/vertical displacement respecfully of the rectangle in pixels from top left corner of screen
                w,h - width and height of rectangle in pixels
                rgb - colors of rectangle in rgb format [0,1]
            output
                Draw a colored rectangle button.
        """

        current_color = gl.glGetFloatv(gl.GL_CURRENT_COLOR)
        gl.glColor3f(r, g, b)
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex2f(x, y)
        gl.glVertex2f(x + w, y)
        gl.glVertex2f(x + w, y + h)
        gl.glVertex2f(x, y + h)
        gl.glEnd()
        gl.glColor3f(*current_color[:3])

    """draw text to screen"""
    def draw_text(self, text, x, y, r, g, b, align="left"):

        """
            inputs
                text - string input
                x,y - x,y horizontal/vertical displacement respecfully of the text in pixels from top left corner of screen
                rgb - colors of text in rgb format [0,1]
                align - "left" "center" "right" alignments for the text
            output
                Draw colored text.
        """

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
