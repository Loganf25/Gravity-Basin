import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame

from pygame.locals import *

from OpenGL.GL import *

from OpenGL.GLU import *

def load_texture(filename):
    #Load an image file as a texture
    texture_surface = pygame.image.load(filename)
    #Convert the image to a string format suitable for OpenGL
    texture_data = pygame.image.tostring(texture_surface, "RGB", True)
    #Get image dimensions
    width = texture_surface.get_width()
    height = texture_surface.get_height()

    #Generate a texture ID and bind it
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)

    #Set texture parameters for wrapping and filtering
    # Repeat the texture in both directions
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    # Use linear filtering for magnification and mipmap linear filtering for minification
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glGenerateMipmap(GL_TEXTURE_2D)

    return texture_id

def draw_sphere(texture_id=None):
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, texture_id)

    #Create sphere object
    #A quadric object is used to define properties for rendering quadric shapes (spheres, cylinders, etc.)
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)

    #Draw sphere with radius 1, 32 slices and 32 stacks
    gluSphere(quadric, 1, 32, 32)

    # Clean up
    gluDeleteQuadric(quadric)
    glPopMatrix()


rotation_x = 0
rotation_y = 0
zoom = 45.0

def main():
    # Initialize Pygame modules
    pygame.init()

    # Set up the display
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    #Depth testing to ensure correct rendering of overlapping objects
    glEnable(GL_DEPTH_TEST)

    #Set ip lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION,  (0, 0, 5, 1)) # light position
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0)) # diffuse light

    #Set up texturing 
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_COLOR_MATERIAL)

    #Earth texture loading
    # Place the texture loading code here
    earth_texture = load_texture("earth.jpg")

    #Enable mouse look variables
    global rotation_x, rotation_y, zoom

    #Hide cursor 
    pygame.mouse.set_visible(True)

    #Lock cursor to window
    pygame.event.set_grab(True)

    #Set up perspective projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(zoom, (display[0]/display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0.0, 0.0, -50)

    # Main loop
    while True:
        for event in pygame.event.get():
            #Quit event handling
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            #Zoom handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: #Scroll up
                    zoom += 0.5
                if event.button == 5: #Scroll down
                    zoom -= 0.5

                #Clamp zoom level
                if zoom < 10: zoom = 10
                if zoom > 1000: zoom = 100

                #Update projection matrix with new zoom level
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                gluPerspective(zoom, (display[0]/display[1]), 0.1, 50.0)
                glMatrixMode(GL_MODELVIEW)
                glTranslatef(0.0, 0.0, -50)

            #Mouse movement handling
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    #Get relative mouse movement
                    mouse_motion_x, mouse_motion_y = event.rel

                    #Update rotation angles based on mouse movement
                    rotation_x += mouse_motion_y * 0.1
                    rotation_y += mouse_motion_x * 0.1

                    #Clamp vertical rotation to avoid flipping
                    if rotation_y > 90: rotation_y = 90
                    if rotation_y < -90: rotation_y = -90

        #Clear screen and depth buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
        #Model View Matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        #Apply rotations based on mouse movement
        glRotatef(rotation_x, 1, 0, 0)  
        glRotatef(rotation_y, 0, 1, 0)

        # Draw the textured sphere
        glPushMatrix()
        glScalef(0.5, 0.5, 0.5)
        glBindTexture(GL_TEXTURE_2D, earth_texture)
        draw_sphere(earth_texture)
        glPopMatrix()


        pygame.display.flip()
        pygame.time.wait(10)
main()
