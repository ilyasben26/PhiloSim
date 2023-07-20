import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self, scale_factor, image_paths, position):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        # load image from proviede image path
        loaded_image_enabled = pygame.image.load(image_paths[0])
        loaded_image_disabled = pygame.image.load(image_paths[1])

        # scale the image and set it
        self.image_enabled = pygame.transform.scale(loaded_image_enabled, (loaded_image_enabled.get_width() * scale_factor, loaded_image_enabled.get_height() * scale_factor))
        self.image_disabled = pygame.transform.scale(loaded_image_disabled, (loaded_image_disabled.get_width() * scale_factor, loaded_image_disabled.get_height() * scale_factor))
        self.image = self.image_enabled
        # set rect
        self.rect = self.image.get_rect()
        # set position
        self.rect.center = position

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def enable(self):
        self.image = self.image_enabled
    
    def disable(self):
        self.image = self.image_disabled