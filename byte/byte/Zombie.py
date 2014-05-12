import PIL
import data
import math
import numpy

import pygame

import Actor
import settings
import utilities

class Zombie(Actor.Actor):
    """
    This is the base class of the Zombie.
    BRAINSSSSSSS
    """
    def __init__(self, game):
        """
        Initialize the zombie parameters.
        """
        Actor.Actor.__init__(self, game, settings.SIMPLE_ZOMBIE_PATH_FORMAT, game.get_zombie_spawn)

    
