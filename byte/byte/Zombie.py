import PIL
import data
import math

import pygame

import Actor
import settings
import utilities

class Zombie(Actor.Actor):
    """
    This is the base class of the Zombie.
    BRAINSSSSSSS
    """
    def __init__(self, game, name="OnlyZombieForNow"):
        """
        Initialize the zombie parameters.
        """
        Actor.Actor.__init__(self, game, settings.SIMPLE_ZOMBIE_PATH_FORMAT, game.get_zombie_spawn)
        
        self.dead = False
        self.dying = False
        self.how_dead = 0
        self.name = name
        self.precise_center = self.rect.center
        
    
    def set_location(self, new_location):
        self.rect.center = new_location
        self.precise_center = new_location
    
    def die(self):
        """
        Oh no I'm dead.
        """
        utilities.log("%s has been shot!" % self.name)
        self.dying = True
    
    def step(self, toward_x, toward_y):
        """
        Move the zombie toward one step.
        """
        elapsed = self.game.clock.get_time() / 1000.0
        
        if self.dying:
            self.image.set_alpha(255 - self.how_dead)
            self.how_dead += 2
            if self.how_dead > 255:
                self.dead = True
            
            return
        
        new_x = self.precise_center[0]
        step = settings.SIMPLE_ZOMBIE_STEP * elapsed
        if toward_x > self.precise_center[0]:
            new_x = self.precise_center[0] + step
        else:
            new_x = self.precise_center[0] - step
        
        new_y = self.precise_center[1]    
        if toward_y > self.precise_center[1]:
            new_y = self.precise_center[1] + step
        else:
            new_y = self.precise_center[1] - step
        
        print (new_x, new_y)
        self.precise_center = (new_x, new_y)
        self.rect.center = (round(new_x), round(new_y))

    
