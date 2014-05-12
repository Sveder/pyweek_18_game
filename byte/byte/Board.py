import data
import math
import numpy

import pygame

import settings
import utilities

class Board(pygame.sprite.Sprite):
    """
    This is the base class of the board who holds the "level" data - background, number of
    zombies, masking of background etc.
    """
    def __init__(self, game):
        """
        Initializes the player ship parameters.
        """
        pygame.sprite.Sprite.__init__(self)
        
        self.game = game
        
        self.image, self.rect = utilities.load_image(data.filepath(settings.BG_IMAGE_PATH))
        self.image.set_alpha(settings.SHOOTER_BG_ALPHA)