import PIL
import data
import math
import numpy

import pygame

import Actor
import settings
import utilities

class Player(Actor.Actor):
    """
    This is the base class of the poor player controlled human who is surely going to be Bytten by zombies.
    """
    def __init__(self, game):
        """
        Initializes the player parameters.
        """
        Actor.Actor.__init__(self, game, settings.PLAYER_IMAGE_PATH_FORMAT, game.get_player_start_position)
        
        pygame.mixer.music.load(data.filepath(settings.PLAYER_SHOT_SOUND))

        
    
    
    def shoot(self, at_x, at_y):
        pygame.mixer.music.play()
        
    