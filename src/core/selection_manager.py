"""Module to handle selection of objects in the scene."""
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLU as glu

class SelectionManager:
    """Class to handle selection of objects in the scene."""
    def __init__(self):
        self.selected_body = None
    def get_ray(self, mouse_x, mouse_y):
        """
        Pick an object based on mouse coordinates. 
        Allows for future improvements, not just clicking planets
        Inputs: 
            mouse_x: X coordinate of mouse
            mouse_y: Y coordinate of mouse
        Returns:
            ray_origin: Origin point of the ray in world coordinates
            ray_direction: Direction vector of the ray in world coordinates
        """
        # Get the current matrices
        modelview = gl.glGetDoublev(gl.GL_MODELVIEW_MATRIX)
        projection = gl.glGetDoublev(gl.GL_PROJECTION_MATRIX)
        viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)

        # Convert mouse coordinates to OpenGL coordinates (x same, y inverted)
        win_x = mouse_x
        win_y = viewport[3] - mouse_y

        # Get the near and far points
        near_point = glu.gluUnProject(win_x, win_y, 0.0, modelview, projection, viewport)
        far_point = glu.gluUnProject(win_x, win_y, 1.0, modelview, projection, viewport)

        # Create a ray from near to far point
        ray_direction = np.array(far_point) - np.array(near_point)
        ray_direction /= np.linalg.norm(ray_direction)

        return np.array(near_point), ray_direction
    def ray_sphere_intersect(self, ray_origin, ray_direction, sphere_center, sphere_radius):
        """
        Check if a ray intersects with a sphere.
        Helper function for pick_object, only true for celestial bodies
        Inputs:
            ray_origin: Origin point of the ray
            ray_direction: Direction vector of the ray (normalized)
            sphere_center: Center point of the sphere
            sphere_radius: Radius of the sphere
        Returns:
            True if the ray intersects the sphere, False otherwise"""
        oc = ray_origin - sphere_center
        a = np.dot(ray_direction, ray_direction)
        b = 2.0 * np.dot(oc, ray_direction)
        c = np.dot(oc, oc) - sphere_radius * sphere_radius
        discriminant = b * b - 4 * a * c
        return discriminant > 0
    def pick_object(self, mouse_x, mouse_y, bodies):
        """
        Pick an object based on mouse coordinates.
        Inputs:
            mouse_x: X coordinate of mouse
            mouse_y: Y coordinate of mouse
            bodies: List of celestial bodies in the scene
        Returns:
            The selected body if any, else None"""
        ray_origin, ray_direction = self.get_ray(mouse_x, mouse_y)

        closest_body = None
        closest_distance = float('inf')

        for body in bodies:
            # Check for sphere intersection (celestial bodies)
            if self.ray_sphere_intersect(ray_origin, ray_direction,
                                         np.array(body.position), body.radius):
                dist = np.linalg.norm(np.array(body.position) - ray_origin)
                if dist < closest_distance:
                    closest_distance = dist
                    closest_body = body
            #Future improvement: else check for other object types here

        self.selected_body = closest_body
        return closest_body
