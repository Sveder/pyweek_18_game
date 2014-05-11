import data
import pygame

import settings
import utilities

class Player(pygame.sprite.Sprite):
    """
    This is the base class of the poor player controlled human who is surely going to be Bytten by zombies.
    """
    def __init__(self, game):
        """
        Initializes the player ship parameters.
        """
        pygame.sprite.Sprite.__init__(self)
        
        self.game = game
        
        #Load the player image:
        image_file_path = settings.PLAYER_IMAGE_PATH
        self.image , self.rect = utilities.load_image(data.filepath(image_file_path))
        
        self.rect.center = self.game.get_player_start_position()
