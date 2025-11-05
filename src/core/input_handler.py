"""Input handling module for the Universe Simulator application."""
import pygame
from core.selection_manager import SelectionManager

class InputHandler:
    """Handles user input events such as mouse movements, clicks, and wheel scrolling."""
    def __init__(self):
        # mouse
        self.mouse_pos = (0, 0)
        self.mouse_pressed = False        # left click pressed (one-frame)
        self.mouse_left_held = False      # left mouse button held state
        self.mouse_right_held = False     # right mouse button held state
        self.last_mouse_pos = None

        # wheel events (one-frame flags)
        self.mouse_wheel_up = False
        self.mouse_wheel_down = False
        self.mouse_wheel_delta = 0        # signed int for scroll amount this frame

        # quit
        self.quit_requested = False

    def process_events(self):
        """Process all pending pygame events and update input states."""
        # reset one-frame flags
        self.mouse_pressed = False
        self.mouse_wheel_up = False
        self.mouse_wheel_down = False
        self.mouse_wheel_delta = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_requested = True

            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # left click
                if event.button == 1:
                    self.mouse_pressed = True
                    self.mouse_left_held = True
                    self.mouse_pos = event.pos
                # wheel up/down on older pygame/backends
                elif event.button == 4:
                    self.mouse_wheel_up = True
                    self.mouse_wheel_delta += 1
                elif event.button == 5:
                    self.mouse_wheel_down = True
                    self.mouse_wheel_delta -= 1
                # right button -> start holding for drag/orbit
                elif event.button == 3:
                    self.mouse_right_held = True
                    self.mouse_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_left_held = False
                if event.button == 3:
                    self.mouse_right_held = False

            # modern pygame wheel event (preferred)
            elif event.type == pygame.MOUSEWHEEL:
                # event.y positive when scrolled up
                if event.y > 0:
                    self.mouse_wheel_up = True
                elif event.y < 0:
                    self.mouse_wheel_down = True
                self.mouse_wheel_delta += event.y

        # if no motion event occurred this frame, keep last position accurate
        # (mouse motion handler keeps mouse_pos updated)
