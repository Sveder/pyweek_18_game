import PIL
import data
import math

import pygame

import Actor
import settings
import utilities

class Player(Actor.Actor):
    """
    This is the base class of the poor player controlled human who is surely going to be Bytten by zombies.
    """
    def __init__(self, game, role=settings.ROLE_NONE):
        """
        Initializes the player parameters.
        """
        utilities.log("Initiated player: %s" % role)
        Actor.Actor.__init__(self, game, settings.PLAYER_IMAGE_PATH_FORMAT, game.get_player_start_position)
        
        pygame.mixer.music.load(data.filepath(settings.PLAYER_SHOT_SOUND))
        pygame.mixer.music.play()
        
        self.role = role
        
    def shoot(self, at_x, at_y):
        utilities.log("Player (%s) is shooting at: %s, %s" % (self.role, at_x, at_y))
        pygame.mixer.music.play()

        
        
class Shooter(Player):
    """
    This is the shooter role - the guy who will shoot zombies but can't actively see them.
    """
    def __init__(self, game):
        Player.__init__(self, game, settings.ROLE_SHOOTER)
    
        
    
class Lighter(Player):
    """
    This is the lighter role - the guy who sees incoming zombies and controls the flashlight for the other player.
    """
    def __init__(self, game):
        Player.__init__(self, game, settings.ROLE_LIGHTER)
    
    
    
    
    
