import PIL
import data
import math

import pygame

import settings
import utilities
from utilities import log

class Actor(pygame.sprite.Sprite):
    """
    Actor in our game. A helper class to load the degree sprites and some turning logic.
    """
    def __init__(self, game, file_path_format, start_position_func=None, sprite_count=360, color_key=(255, 255, 255)):
        """
        Load all the degree logic.
        """
        pygame.sprite.Sprite.__init__(self)
        log("Creating an actor with file format: %s" % file_path_format)
        
        self.game = game
        
        #load all the angle images:
        self.sprite_count = sprite_count
        self.angle_pictures = []
        for i in xrange(self.sprite_count):
            image, _ = utilities.load_image(data.filepath(file_path_format % i))
            image.set_colorkey(color_key)
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
        self._cur_angle = int(round(-angle_to_pointer)) + 90
        self._cur_angle %= self.sprite_count
        self.image = self.angle_pictures[self._cur_angle]
        
        self.rect = self.image.get_rect()
        self.rect.center = old_rect.center
        

class PlayerActor(pygame.sprite.Sprite):
    """
    Actor in our game. A helper class to load the degree sprites and some turning logic.
    """
    def __init__(self, game, file_path_format, start_position_func=None, sprite_count=360, color_key=(255, 255, 255)):
        """
        Load all the degree logic.
        """
        pygame.sprite.Sprite.__init__(self)
        log("Creating an actor with file format: %s" % file_path_format)
        
        self.game = game
        self.color_key = color_key
        self.angle_position = []
        #load all the angle images:
        self.sprite_count = sprite_count
        self.angle_pictures = []
        for i in xrange(self.sprite_count):
            sprite_sheet = utilities.spritesheet(data.filepath(file_path_format % i))
            position = settings.SPRITE_PLAYER_POSITIONS[i]
            for j in xrange(360 / 15):
                self.angle_pictures.append(sprite_sheet)
                self.angle_position.append(position)
        
        self._cur_angle = 0
        self.shot_frame = 0
        
        positions = self.angle_position[self._cur_angle][int(self.shot_frame)]
        rect = pygame.Rect(positions[0], 0, positions[1] - positions[0], 51)
        self.image = self.angle_pictures[self._cur_angle].image_at(rect, colorkey=self.color_key)
        
        self.rect = rect
        
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
        self._cur_angle = int(round(-angle_to_pointer))
        self._cur_angle %= 360
        
        positions = self.angle_position[self._cur_angle][int(self.shot_frame)]
        rect = pygame.Rect(positions[0], 0, positions[1] - positions[0], 51)
        self.image = self.angle_pictures[self._cur_angle].image_at(rect, colorkey=self.color_key)
        
        self.rect = rect
        self.rect.center = old_rect.center
    

class SpriteActor(pygame.sprite.Sprite):
    """
    Actor in our game. A helper class to load the sprite sheet and handle degrees.
    """
    def __init__(self, game, spritesheet, start_position_func=None):
        """
        Load all the degree logic.
        """
        pygame.sprite.Sprite.__init__(self)
        log("Creating an actor with file format: %s" % file_path_format)
        
        self.game = game
        
        self._cur_angle = 0
        
        spritesheet_file = random.choice(settings.ZOMBIE_SPRITES)
        spritesheet_file = data.filepath(spritesheet_file_name)
        spritesheet = utilities.spritesheet(spritesheet_file)
        
        
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