import pygame

class TransitionTrigger(pygame.sprite.Sprite):
    def __init__(self, pos, groups, callback_function):
        super().__init__(groups)
        self.image = pygame.Surface((50, 50))  # Adjust size as needed
        self.image.fill((255, 0, 0))  # Red color for visualization
        self.rect = self.image.get_rect(topleft=pos)
        self.callback_function = callback_function

    def update(self):
        # Check for collision with the player
        if pygame.sprite.spritecollide(self, self.groups()[0], False):
            self.callback_function()