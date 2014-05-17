import PIL
import data
import math
import random

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
        sprite_format = random.choice(settings.SIMPLE_ZOMBIE_FORMATS)
        Actor.Actor.__init__(self, game, sprite_format, game.get_zombie_spawn)
        
        self.dead = False
        self.dying = False
        self.how_dead = 0
        self.name = name
        self.precise_center = self.rect.center
        self.speed = random.choice(settings.SIMPLE_ZOMBIE_STEP_RANGE)
        
        pygame.mixer.Sound(data.filepath(settings.ZOMBIE_SPAWN_SOUND)).play()
        
        
    def set_location(self, new_location):
        self.rect.center = new_location
        self.precise_center = new_location
    
    def set_speed(self, speed):
        self.speed = speed
    
    
    def die(self):
        """
        Oh no I'm dead.
        """
        if self.dead or self.dying: return
        
        utilities.log("%s has been shot!" % self.name)
        self.dying = True
        pygame.mixer.Sound(data.filepath(settings.ZOMBIE_DEATH_SOUND)).play()
    
    
    def step(self, toward_x, toward_y):
        """
        Move the zombie toward one step.
        """
        if self.dead: return
        
        elapsed = self.game.clock.get_time() / 1000.0
        
        if self.dying:
            self.image.set_alpha(255 - self.how_dead)
            self.how_dead += 2

            if self.how_dead > 255:
                self.dead = True
            
            return
        
        new_x = self.precise_center[0]
        step = self.speed * elapsed * self.game.scale_zombies 
        
        if toward_x > self.precise_center[0]:
            new_x = self.precise_center[0] + step
        else:
            new_x = self.precise_center[0] - step
        
        new_y = self.precise_center[1]    
        if toward_y > self.precise_center[1]:
            new_y = self.precise_center[1] + step
        else:
            new_y = self.precise_center[1] - step
        
        self.precise_center = (new_x, new_y)
        self.rect.center = (round(new_x), round(new_y))

    
