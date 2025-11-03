
import pygame

class InputHandler:
    def __init__(self):
        self.mouse_pos = (0, 0)
        self.mouse_pressed = False
        self.quit_requested = False

    def process_events(self):
        self.mouse_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_requested = True
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_pressed = True
