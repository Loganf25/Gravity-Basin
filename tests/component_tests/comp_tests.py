import pytest
from src.core.engine import Engine
from src.simulation.models.planet import Planet
from src.core.states import States
from src.simulation.models.celestial_body import CelestialBody
from src.ui.main_menu import MainMenu
from src.core.input_handler import InputHandler
from src.ui.hud import SimulationScreen
from src.simulation.data import simulation_data
from src import main

"""Component tests for the Universe Simulator
Test Inteactions between core.engine and other bodies
This is the main interaction point of the program"""


#Flows to test: 
class componentTests:
    def __init__(self):
        self.engine = Engine()
        self.main_menu = MainMenu(self.engine)
        self.planet = Planet("Earth")
        self.hud = SimulationScreen(self.engine)
        
    #engine -- states
    def engine_state(self):
        self.engine.change_state(States.EXIT)
        assert self.engine.state == States.EXIT
        
    #engine -- input_handler
    def engine_inputHandler(self):
        self.engine.handle_sim_input() # calls input manager
        
    #engine -- time_manager
    def engine_timeManager(self):
        self.engine.change_state(States.SIMULATION) # calls time-management
        
    #engine -- selection_manager
    def engine_selectionManager(self):
        self.engine.selection_manager.current_body = self.planet
        self.engine.delete_selected_body()       
    
    #engine -- main_menu -- states
    def engine_mainMenu_states(self):
        self.main_menu.update(InputHandler())
        
    #engine -- hud -- states
    def engine_hud_states(self):
        self.hud.update(InputHandler())
        
    #engine -- renderer
    def engine_renderer(self):
        self.engine.initialize_simulation()
        
    #engine -- camera
    def engine_camera(self):
        self.engine.handle_sim_input()
        
    #engine -- texture_loader
    def engine_textureLoader(self):
        self.engine.initialize_simulation()
        
    #engine -- orbit_service
    def engine_orbitService(self):
        self.engine.populate_scene()
        
    #engine -- physics_service
    def engine_physicsService(self):
        self.engine.populate_scene()
        
    #engine -- simulation_data -- physics_service
    def engine_simulationData_PhysicsService(self):
        self.engine.populate_scene()
        
    #engine -- planet
    def engine_planet(self):
        self.engine.populate_scene()
        
    #planet -- simulation_data
    def planet_simulationData(self):
        simulation_data.get_planet_data("Earth")
        
    #main   -- engine
    def main_engine(self):
        main.main()
        
    @pytest.fixture
    def componentTest(self):
        self.engine_state()
        self.engine_inputHandler()
        self.engine_timeManager()
        self.engine_selectionManager()
        self.engine_mainMenu_states()
        self.engine_hud_states()
        self.engine_renderer()
        self.engine_camera()
        self.engine_textureLoader()
        self.engine_orbitService()
        self.engine_physicsService()