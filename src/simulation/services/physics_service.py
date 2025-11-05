"""handles gravitational updates and manages the running simulation state"""

import math
import time

#G = 6.67430e-11  # gravitational constant (m^3 kg^-1 s^-2)
G = 1.0  # scaled gravitational constant for simulation

class PhysicsService:
    """Service to manage physics simulation including gravitational interactions."""
    def __init__(self):
        self.bodies = []
        self.is_running = False
        self.last_update = None
        self.time_scale = 1.0  # multiplier for sim speed

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

        distance_sq = dx*dx + dy*dy + dz*dz
        distance = math.sqrt(distance_sq)

        if distance == 0:
            return [0.0, 0.0, 0.0]

        force_mag = G * body1.mass * body2.mass / distance_sq
        fx = force_mag * dx / distance
        fy = force_mag * dy / distance
        fz = force_mag * dz / distance

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
                fx, fy, fz = self.compute_gravitational_force(b1, b2)

                forces[b1][0] += fx
                forces[b1][1] += fy
                forces[b1][2] += fz

                forces[b2][0] -= fx
                forces[b2][1] -= fy
                forces[b2][2] -= fz

        # update all bodies
        for body in self.bodies:
            fx, fy, fz = forces[body]
            ax = fx / body.mass
            ay = fy / body.mass
            az = fz / body.mass

            body.velocity[0] += ax * delta_time
            body.velocity[1] += ay * delta_time
            body.velocity[2] += az * delta_time

            body.position[0] += body.velocity[0] * delta_time
            body.position[1] += body.velocity[1] * delta_time
            body.position[2] += body.velocity[2] * delta_time

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
