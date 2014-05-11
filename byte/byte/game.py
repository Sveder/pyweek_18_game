import data

import pygame

import settings
import utilities

class Game:
    def __init__(self):
        """
        Initialize the game objects and pygame.
        """
        pygame.init()
        
        self.clock = pygame.time.Clock()
        
        self.screen = None
        
            
    def start(self):
        """
        Start the game and then pass control to the main loop. Open the window, put everything in the
        needed position and start the game loop.
        """
        #Initialize the gameboard class and screen:
        self.screen = pygame.display.set_mode(settings.SCREEN_SIZE, 0)
        self.screen.fill(settings.BACKGROUND_FILL_COLOR)
        
        
    
    

def start():
    utilities.log("Game started!")
    game = Game()
    game.start()
    utilities.log("Game ended!")