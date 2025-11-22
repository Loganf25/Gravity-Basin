"""Component tests for the Universe Simulator
Test Inteactions between core.engine and other bodies
This is the main interaction point of the program

Flows to test:
engine -- states
engine -- input_handler
engine -- time_manager
engine -- selection_manager
engine -- main_menu -- states
engine -- hud -- states
engine -- renderer
engine -- camera
engine -- texture_loader
engine -- orbit_service
engine -- physics_service
engine -- simulation_data -- physics_service
engine -- planet
engine -- star
star   -- celestial_body
planet -- celestial_body
star   -- simulation_data
planet -- simulation_data
main   -- engine"""
