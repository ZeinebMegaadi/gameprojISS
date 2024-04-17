import pygame

class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('cursor-export.png').convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        # Update the cursor position to the mouse position
        self.rect.topleft = pygame.mouse.get_pos()