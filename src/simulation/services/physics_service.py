"""handles gravitational updates and manages the running simulation state"""

import math
import time

G = 6.67430e-11  # gravitational constant (m^3 kg^-1 s^-2)
AU_IN_METERS = 1.496e11  # astronomical unit in meters
VISUAL_TO_METERS = 1.0 / 8.0 

class PhysicsService:
    """Service to manage physics simulation including gravitational interactions."""
    def __init__(self):
        self.bodies = []
        self.is_running = False
        self.last_update = None
        self.time_scale = 3e6  # scale real time to simulation time

    def register_body(self, body):
        """Add a celestial body to the simulation."""
        self.bodies.append(body)

    def clear_bodies(self):
        """Remove all bodies from the simulation."""
        self.bodies = []

    def start(self):
        """Start the simulation."""
        if not self.is_running:
            self.is_running = True
            self.last_update = time.time()

    def pause(self):
        """Pause the simulation."""
        self.is_running = False

    def toggle(self):
        """Toggle the simulation running state."""
        self.is_running = not self.is_running
        if self.is_running:
            self.last_update = time.time()

    def reset(self):
        """Reset the simulation to initial state."""
        self.clear_bodies()
        self.is_running = False
        self.last_update = None

    def compute_gravitational_force(self, body1, body2):
        """Compute gravitational force exerted on body1 by body2."""
        dx = body2.position[0] - body1.position[0]
        dy = body2.position[1] - body1.position[1]
        dz = body2.position[2] - body1.position[2]

        #Changed to use distance squared for force calculation in meters
        distance_m = math.sqrt(dx**2 + dy**2 + dz**2) * VISUAL_TO_METERS * AU_IN_METERS

        if distance_m == 0:
            return [0.0, 0.0, 0.0]

        force_mag = G * body1.mass * body2.mass / distance_m**2
        fx = force_mag * dx / math.sqrt(dx*dx + dy*dy + dz*dz)
        fy = force_mag * dy / math.sqrt(dx*dx + dy*dy + dz*dz)
        fz = force_mag * dz / math.sqrt(dx*dx + dy*dy + dz*dz)

        return [fx, fy, fz]

    def step(self, delta_time):
        """Advance the simulation by delta_time seconds."""
        # physics integration step
        forces = {body: [0.0, 0.0, 0.0] for body in self.bodies}

        # accumulate forces
        for i in range(len(self.bodies)):
            for j in range(i + 1, len(self.bodies)):
                b1 = self.bodies[i]
                b2 = self.bodies[j]
                force_vector = self.compute_gravitational_force(b1, b2)

                forces[b1][0] += force_vector[0]
                forces[b1][1] += force_vector[1]
                forces[b1][2] += force_vector[2]

                forces[b2][0] -= force_vector[0]
                forces[b2][1] -= force_vector[1]
                forces[b2][2] -= force_vector[2]

        # update all bodies
        for body in self.bodies:
            if body.mass == 0:
                continue  # skip massless bodies

            ax = forces[body][0] / body.mass
            ay = forces[body][1] / body.mass
            az = forces[body][2] / body.mass

            body.velocity[0] += ax * delta_time
            body.velocity[1] += ay * delta_time
            body.velocity[2] += az * delta_time

            body.position[0] += (body.velocity[0] * delta_time) / (AU_IN_METERS * VISUAL_TO_METERS)
            body.position[1] += (body.velocity[1] * delta_time) / (AU_IN_METERS * VISUAL_TO_METERS)
            body.position[2] += (body.velocity[2] * delta_time) / (AU_IN_METERS * VISUAL_TO_METERS)

            if hasattr(body, 'trail'):
                body.trail.append(tuple(body.position))

    def update(self):
        """Update the simulation state based on elapsed time."""
        if not self.is_running:
            return

        current_time = time.time()
        if self.last_update is None:
            self.last_update = current_time
            return

        delta_time = (current_time - self.last_update) * self.time_scale
        self.last_update = current_time

        self.step(delta_time)

    def set_time_scale(self, scale):
        """Set the time scale for the simulation."""
        self.time_scale = max(0.0, scale)
