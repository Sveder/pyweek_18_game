import data

import pygame

import settings
import utilities
from utilities import log

class Bullet(pygame.sprite.Sprite):
    """
    A bullet container.
    """
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        
        self.image, self.rect = utilities.load_image(data.filepath(settings.BULLET_IMAGE_PATH))
        self.image.set_colorkey((255, 255, 255))

    
    def render_bullets(self, count):
        surface = pygame.Surface((self.rect.width * count, self.rect.height))
        for c in xrange(count):
            surface.blit(self.image, (self.rect.width * c, 0))
        
        return surface
        