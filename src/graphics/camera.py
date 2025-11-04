"""module for camera control in a 3D OpenGL environment"""
import math
from OpenGL.GLU import gluLookAt

class Camera:
    """Dynamic camera for orbiting and zooming around a target point."""
    def __init__(self):
        self.distance = 25.0       # initial zoom distance
        self.azimuth = 45.0
        self.elevation = 15.0
        self.target = [0.0, 0.0, 0.0]

        self.rotate_speed = 0.25
        self.zoom_factor = 1.1     # multiplicative zoom
        self.min_distance = 0.1    # optional small floor
        self.max_distance = 10**30 # practically uncapped

        self._last_mouse = None

    def handle_input(self, input_handler):
        """Update camera position based on input handler state."""
        # zoom with multiplicative factor
        if input_handler.mouse_wheel_delta != 0:
            if input_handler.mouse_wheel_delta > 0:  # scroll up -> zoom in
                self.distance /= self.zoom_factor ** input_handler.mouse_wheel_delta
            else:                                   # scroll down -> zoom out
                self.distance *= self.zoom_factor ** -input_handler.mouse_wheel_delta

            # enforce min/max distance
            self.distance = max(self.min_distance, min(self.max_distance, self.distance))

        # orbit with right button held
        if input_handler.mouse_right_held:
            if self._last_mouse is None:
                self._last_mouse = input_handler.mouse_pos
            else:
                mx, my = input_handler.mouse_pos
                lx, ly = self._last_mouse
                dx = mx - lx
                dy = my - ly

                self.azimuth += dx * self.rotate_speed
                self.elevation += -dy * self.rotate_speed
                self.elevation = max(-89.9, min(89.9, self.elevation))

                self._last_mouse = input_handler.mouse_pos
        else:
            self._last_mouse = None

    def apply(self):
        """Apply the camera transformation using gluLookAt."""
        az = math.radians(self.azimuth)
        el = math.radians(self.elevation)

        cx = self.target[0] + self.distance * math.cos(el) * math.sin(az)
        cy = self.target[1] + self.distance * math.sin(el)
        cz = self.target[2] + self.distance * math.cos(el) * math.cos(az)

        gluLookAt(cx, cy, cz,
                  self.target[0], self.target[1], self.target[2],
                  0.0, 1.0, 0.0)
