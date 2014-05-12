import PIL
import data
import math
import numpy

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
        image_file_path = settings.PLAYER_IMAGE_PATH_FORMAT
        
        
        #load all the angle images:
        self.angle_pictures = []
        for i in xrange(365):
            image, _ = utilities.load_image(data.filepath(image_file_path % i))
            image.set_colorkey((255, 255, 255))
            self.angle_pictures.append(image)
        
        self._cur_angle = 0
        self.image = self.angle_pictures[self._cur_angle]
        self.rect = self.image.get_rect()
        self.rect.center = self.game.get_player_start_position()
    
    
    def turn(self, towards_x, towards_y):
        """
        Turn the player towards the point whose coordinates are given.
        """
        angle_to_pointer = math.degrees(math.atan2(towards_y - self.rect.center[1], towards_x - self.rect.center[0]))


        #Append the rect to move/delete:
        old_rect = self.rect
        self.game.dirty_rects.append(old_rect)
        
        #Find the new angle and replace the image:
        self._cur_angle = int(round(-angle_to_pointer)) - 90
        self._cur_angle %= 360
        self.image = self.angle_pictures[self._cur_angle]
        
        self.rect = self.image.get_rect()
        self.rect.center = old_rect.center
    
