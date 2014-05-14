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
        self.slower = 0
        
        
    
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
        if self.dying:
            self.image.set_alpha(255 - self.how_dead)
            self.how_dead += 3
            if self.how_dead > 255:
                self.dead = True
            
            return
        
        self.slower += 1
        if self.slower % 7:
            return
        
        new_x = self.rect.center[0]
        if toward_x > self.rect.center[0]:
            new_x = (self.rect.center[0] + settings.SIMPLE_ZOMBIE_STEP)
        else:
            new_x = self.rect.center[0] - settings.SIMPLE_ZOMBIE_STEP
        
        new_y = self.rect.center[1]    
        if toward_y > self.rect.center[1]:
            new_y = self.rect.center[1] + settings.SIMPLE_ZOMBIE_STEP
        else:
            new_y = self.rect.center[1] - settings.SIMPLE_ZOMBIE_STEP
            
        self.rect.center = (new_x, new_y)

    
