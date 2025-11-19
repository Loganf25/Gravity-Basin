"""Time management for the simulation."""
import pygame

class TimeManager:
    """Manages time-related functionalities for the simulation."""

    def __init__(self):
        #Variables
        #Actual sim time scale
        self.paused = True
        self.sim_scale = 0.0  #Current simulation time scale
      
        #Base time scale factor (e.g., 3 million sim seconds per real second)
        self.base_time_scale = 3e6  #(35 sim days per real second, same as physics_service default)

        #User adjustable multiplier (the adjustable speed factor)
        self.time_multiplier = 1.0

        #For time scale rather than fixed steps
        self.min_time_mult = 0.125  # Minimum time scale
        self.max_time_mult = 8  # Maximum time scale

    def update(self, d_real_sec):
        """
        Update the simulation time based on real elapsed time.
        Input:
            d_sim_sec: Elapsed simulation time in seconds.
        Output:
            Simulation seconds to advance physics calculations.
        """
        #Handle paused state
        if self.paused:
            return 0.0

        #Calculate time that has passed
        #Sim speed will be the real time passed (as thats what we have)
        #Multiply by base scale (to get 35 days/sec, 1 sec/sec is TOO SLOW)
        #and user multiplier to get final wanted speed
        d_sim_sec = d_real_sec * self.base_time_scale * self.time_multiplier

        #Add change to current sim scale (slowing down will be negative)
        self.sim_scale += d_sim_sec

        #Update returned for physics step
        return d_sim_sec

    def toggle_pause(self):
        """Toggle the paused state of the simulation.
        This will be called by the buttons in the UI."""
        self.paused = not self.paused

    def increase_speed(self):
        """Increase the simulation speed multiplier by 2."""
        if self.time_multiplier < self.max_time_mult:
            self.time_multiplier *= 2.0

    def decrease_speed(self):
        """Decrease the simulation speed multiplier by 2."""
        if self.time_multiplier > self.min_time_mult:
            self.time_multiplier /= 2.0

    def get_scale(self):
        """Get the current simulation time scale in seconds per real second."""
        if self.paused:
            return 0.0
        return self.base_time_scale * self.time_multiplier

    def get_status_text(self):
        """Get the current status text for HUD."""
        status = "Paused" if self.paused else "Running"
        return f"{status} ({self.time_multiplier}x)"

    