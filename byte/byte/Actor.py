import PIL
import data
import math
import numpy

import pygame

import settings
import utilities
from utilities import log

class Actor(pygame.sprite.Sprite):
    """
    Actor in our game. A helper class to load the degree sprites and some turning logic.
    """
    def __init__(self, game, file_path_format, start_position_func=None):
        """
        Load all the degree logic.
        """
        pygame.sprite.Sprite.__init__(self)
        log("Creating an actor with file format: %s" % file_path_format)
        
        self.game = game
        
        #load all the angle images:
        self.angle_pictures = []
        for i in xrange(365):
            image, _ = utilities.load_image(data.filepath(file_path_format % i))
            image.set_colorkey((255, 255, 255))
            self.angle_pictures.append(image)
        
        self._cur_angle = 0
        self.image = self.angle_pictures[self._cur_angle]
        self.rect = self.image.get_rect()
        
        if start_position_func:
            self.rect.center = start_position_func()

    
    
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
    
