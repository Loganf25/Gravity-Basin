"""Core engine module for the Universe Simulator application."""
import math
from collections import deque
import pygame
import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
from core.states import States
from core.input_handler import InputHandler
from core.time_manager import TimeManager
from core.selection_manager import SelectionManager
from ui.main_menu import MainMenu
from ui.hud import SimulationScreen
from graphics.renderer import Renderer
from graphics.camera import Camera
from graphics.texture_loader import TextureLoader
from simulation.services.orbit_service import OrbitService
from simulation.services.physics_service import PhysicsService, G, AU_IN_METERS
from simulation.data.simulation_data import planet_textures, PLANET_DATA
from simulation.models.planet import Planet
#from simulation.models.star import Star


AU_VISUAL_SCALE = 8.0
RADIUS_VISUAL_SCALE = 0.0001

class Engine:
    """Core engine to run the Universe Simulator application."""
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((1280, 720), pygame.OPENGL | pygame.DOUBLEBUF)
        glut.glutInit()
        pygame.display.set_caption("Universe Simulator")

        self.clock = pygame.time.Clock()
        self.running = True
        self.time_manager = TimeManager()
        self.input_handler = InputHandler()
        self.state = States.MENU 

        self.physics_service = PhysicsService()
        self.texture_loader = TextureLoader()
        self.orbit_service = OrbitService(self.physics_service)
        self.renderer = Renderer(self.texture_loader)

        self.camera = Camera()  # dynamic camera instance

        self.textures_initialized = False
        self.selection_manager = SelectionManager()
        self.main_menu = MainMenu(self)
        self.sim_screen = SimulationScreen(self)

        self.setup_opengl()

    def setup_opengl(self):
        """Setup basic OpenGL state."""
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDepthFunc(gl.GL_LEQUAL)
        gl.glViewport(0, 0, 1280, 720)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(60, 1280/720, 0.1, 10000.0) #Last vlaue is render distance
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)


    def populate_scene(self, i = -1):
        """Create Sun and planets, scale for visualization, and register with PhysicsService.

        This implementation uses the Planet factory and keeps visualization-only
        attributes (trail, visual radius, position) in the engine. It avoids
        creating ad-hoc objects or assigning attributes to unknown types.
        """

        if i == -1:

            self.physics_service.clear_bodies() #clear every planet out incase of reset

            # Create and register each planet using the Planet model
            for pdata in PLANET_DATA:
                planet = self._create_planet(pdata)
                if planet is not None:
                    self.physics_service.register_body(planet)

            # After all bodies are registered, compute orbits using the Sun as center
            sun = next((b for b in self.physics_service.bodies if getattr(b, "name", "").lower() == "sun"), None)
            if not sun:
                return
            for body in self.physics_service.bodies:
                if body is not sun:
                    self.orbit_service.compute_orbit(body, sun, AU_VISUAL_SCALE)
        else:
            # Create and register each planet using the Planet model
            for j in range(len(PLANET_DATA)):
                planet = self._create_planet(PLANET_DATA[j])
                if planet is not None and j == i:
                    self.physics_service.register_body(planet)
                    print("manually spawned ",PLANET_DATA[j])

    def _create_planet(self, pdata):
        """Create a Planet instance from planet data and add visualization attrs.

        Returns Planet instance or None on failure.
        """
        try:
            p = Planet(pdata["name"])
        except (ValueError, AttributeError) as exc:
            # Log and skip planets that can't be constructed from data
            print(f"Warning: could not construct Planet '{pdata.get('name')}' - {exc}")
            return None

        # Trail length: 75% of orbital frames; minimum handled below
        if pdata["name"].lower() != "sun":
            trail_len = self._calculate_trail_length(pdata)
            p.trail = deque(maxlen=max(50, trail_len))
        else:
            p.trail = deque(maxlen=0)

        # Position (visual units)
        p.position = [pdata["distance_from_sun"] * AU_VISUAL_SCALE, 0.0, 0.0]
        p.initial_position = list(p.position)

        # Visual radius scaling (keeps original radius value on model untouched)
        base_radius = pdata.get("radius", 1.0) * RADIUS_VISUAL_SCALE
        if pdata["name"].lower() == "sun":
            p.radius = max(1.0, base_radius * 20.0)
        else:
            p.radius = max(0.5, base_radius)

        return p

    def delete_selected_body(self):
        if self.selection_manager.get_selected_body() is not None:
            self.physics_service.bodies.remove(self.selection_manager.get_selected_body())

    def _calculate_trail_length(self, pdata):
        """Calculate trail length (frames) based on orbital period and time scale."""
        sun_mass = next((d["mass"] for d in PLANET_DATA if d["name"].lower() == "sun"), None)
        if sun_mass is None:
            return 50

        distance_m = pdata["distance_from_sun"] * AU_IN_METERS
        orbital_period_s = 2 * math.pi * math.sqrt(distance_m**3 / (G * sun_mass))

        # Convert orbital period seconds to number of simulation frames
        sim_time_per_frame = self.time_manager.get_scale() * (1.0/60.0)  #assuming 60 FPS
        if sim_time_per_frame == 0:
            return 0  # avoid division by zero; no trail when paused
        frames_for_full_orbit = orbital_period_s / sim_time_per_frame
        return int(0.75 * frames_for_full_orbit)


    def render_ui_overlay(self, draw_fn):
        """Render a UI overlay by switching to orthographic projection."""
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        gl.glOrtho(0, 1280, 720, 0, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glDisable(gl.GL_LIGHTING)
        draw_fn()
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPopMatrix()
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPopMatrix()

    def handle_sim_input(self):
        """Handle input specific to the simulation state."""
        self.camera.handle_input(self.input_handler)

        if self.input_handler.mouse_pressed:
            self.selection_manager.pick_object(self.input_handler.mouse_pos[0],
                                               self.input_handler.mouse_pos[1],
                                               self.physics_service.bodies)
        if self.selection_manager.selected_body:
            #Sets the camera target to the selected body, making it the center
            self.camera.target = self.selection_manager.selected_body.position

    def initialize_simulation(self):
        """Initializes textures and populates the scene."""
        if not self.textures_initialized:
            print("Initializing planet textures...")
            
            # only load textures if no texture loading exception occurs
            self.texture_loader.initialize_textures(planet_textures)
            if (self.texture_loader.textures_loaded):
                self.renderer.initialize_textures(planet_textures)
                self.populate_scene()
                self.textures_initialized = True
                print("Textures and scene populated successfully.")
            else:
                print("Textures failed to load.")
                self.running = False
                return

    def state_switch(self, state):
        if state == States.MENU:
            self.render_ui_overlay(lambda: (self.main_menu.update(self.input_handler),
                                            self.main_menu.render()))
        elif state == States.SIMULATION:
            self.handle_sim_input()
            #Time management
            d_real_sec = self.clock.get_time() / 1000.0  # get elapsed real time in seconds
            d_sim_sec = self.time_manager.update(d_real_sec) # get simulation time to advance
            self.physics_service.update(d_sim_sec) # update physics with simulation time step
            self.sim_screen.update_label(self.time_manager.get_status_text(), 0)

            self.renderer.render(self.physics_service, self.camera)
            self.render_ui_overlay(lambda: (self.sim_screen.update(self.input_handler),
                                            self.sim_screen.render()))
        elif state == States.CREDITS:
            self.main_menu.draw_credits()
        elif state == States.EXIT:
            self.exit()
        elif state == States.PAUSE:
            self.pause()
        
    

    def run(self):
        """Main loop of the engine."""
        self.initialize_simulation()
        while self.running:
            self.input_handler.process_events()
            self.state_switch(state=self.state)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
    
    def exit(self):
        self.running = False

    def change_state(self, new_state):
        """Change the current state of the engine."""
        if new_state in States: # check to see if new state is member of enum
            self.state_switch(new_state)
        else: # failed type-check
            # TODO: add logging
            print("Error! Invalid state: " + new_state)    
        
        self.state = new_state
        