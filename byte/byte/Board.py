import data
import math
import random

import pygame

import settings
import utilities

BRIGHTEN_RECT_TEMP = 120
HALF_RECT_TEMP = BRIGHTEN_RECT_TEMP / 2

class Board(pygame.sprite.Sprite):
    """
    This is the base class of the board who holds the "level" data - background, number of
    zombies, masking of background, music etc.
    """
    def __init__(self, game):
        """
        Initializes the player ship parameters.
        """
        pygame.sprite.Sprite.__init__(self)
        
        self.game = game
        
        self.unmasked_image, self.rect = utilities.load_image(data.filepath(settings.UNMASKED_BG_IMAGE_PATH))
        self.masked_image, _= utilities.load_image(data.filepath(settings.MASKED_BG_IMAGE_PATH))
        
        self.image = self.masked_image.copy()
        self.image.set_colorkey((255, 255,0))
        
        self.last_brighten = (0, 0)
        
        #Load music and ambient sound:
        self.tracks = []
        self.cur_track = 0
        for track in settings.MUSIC_TRACKS:
            sound = pygame.mixer.Sound(data.filepath(track))
            self.tracks.append(sound)
            
        self.start_music()
        
        self.ambient_sounds = []
        for i in settings.AMBIENT_SOUNDS:
            self.ambient_sounds.append(pygame.mixer.Sound(data.filepath(i)))
        #Schedule an ambient event about every two minutes:
        pygame.time.set_timer(settings.SCHEDULE_AMBIENT_EVENT, 2 * 60 * 1000)
        
    
    def unmask(self, near_x, near_y, radius=BRIGHTEN_RECT_TEMP):
        """
        Brighten (unmask) the area near the given coordinates.
        """
        self._actual_unmask(self.last_brighten, self.masked_image, radius=radius)
        
        brighten_rect = pygame.draw.circle(self.image, (255, 255,0), (near_x, near_y), radius/2)
        self.game.dirty_rects.append(brighten_rect)
        
        self.last_brighten = (near_x, near_y)
    

    def _actual_unmask(self, (near_x, near_y), surface, radius=BRIGHTEN_RECT_TEMP):
        rect = pygame.Rect(near_x - radius/2, near_y - radius/2, radius, radius)
        self.image.blit(surface, rect, rect)
        self.game.dirty_rects.append(rect)
    
    
    def triangular_unmask(self, near_x, near_y, player):
        p_center = player.rect.center
        
        
        
        
    def start_music(self):
        channel = self.tracks[self.cur_track].play()
        channel.set_endevent(settings.MUSIC_ENDED_EVENT)
        self.cur_track += 1
        self.cur_track %= len(self.tracks)
        
        
    def play_ambient(self):
        sound = random.choice(self.ambient_sounds)
        sound.set_volume(0.8)
        sound.play()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        