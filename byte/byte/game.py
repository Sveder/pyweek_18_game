import data

import pygame

import Board
import Player
import settings
import utilities
from utilities import log

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
        #Initialize pygame window:
        self.screen = pygame.display.set_mode(settings.SCREEN_SIZE, 0)
        
        self.board = Board.Board(self)
        self.screen.blit(self.board.image, self.board.rect)

        
        self.player = Player.Player(self)
        self.screen.blit(self.player.image, self.player.rect)
        
        self.dirty_rects = []
        
        pygame.display.update()
        self.main_loop()
        
    
    def main_loop(self):
        """
        The main loop of the game, where most of the fun happens.
        """
        while 1:
            self.clock.tick()
            
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    log("Player exited!")
                    return
                
            self.turn_player_towards_mouse()
            self.screen.blit(self.board.image, self.board.rect)
            self.screen.blit(self.player.image, self.player.rect)
            
            if self.dirty_rects:
                pygame.display.update(self.dirty_rects)
            
            
            self.dirty_rects = []

            print self.clock.get_fps()




            
        
    def turn_player_towards_mouse(self):
        """
        Turn the player sprite towards the mouse.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.player.turn(mouse_x, mouse_y)
        
    
    def get_player_start_position(self):
        """
        The player initial position is probably the center. Mostly?
        """
        return self.screen.get_rect().center
    
    

def start():
    utilities.log("Game started!")
    game = Game()
    game.start()
    utilities.log("Game ended!")