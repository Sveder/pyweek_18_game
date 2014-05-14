import data
import threading

import pygame

import Board
import Player
import Zombie
import net_code
import settings
import utilities
from utilities import log

ip = "localhost"
port = 6317


class Game:
    def __init__(self, host, port, is_server=True, role=settings.ROLE_LIGHTER):
        """
        Initialize the game objects and pygame.
        """
        pygame.init()
        
        self.clock = pygame.time.Clock()
        self.screen = None
        
        #Remote server communicates using sockets and the net code adds events to this list:
        self.event_list = []
        self.event_list_lock = threading.Lock()
        
        self.role = role
        self.host = host
        self.port = port
        self.is_server = is_server
        
        #This will definitely move soon:
        if is_server:
            self.net_object = net_code.Server()
            self.net_thread = threading.Thread(target=self.net_object.start, args=[self])
        else:
            self.net_object = net_code.Client()
            self.net_thread = threading.Thread(target=self.net_object.connect, args=[self])
        
        self.net_thread.start()
            
        
    def create_player(self):
        """
        Figure out which role the player is and initiate the right class.
        """
        if self.role == settings.ROLE_LIGHTER:
            self.player = Player.Lighter(self)
        elif self.role == settings.ROLE_SHOOTER:
            self.player = Player.Shooter(self)
        else:
            raise Exception("Role is not a valid player role: %s." % self.role)
        
        log("Initialized a game with role: %s" % self.role)
        
        
    def start(self):
        """
        Start the game and then pass control to the main loop. Open the window, put everything in the
        needed position and start the game loop.
        """
        self.dirty_rects = []
        
        #Initialize pygame window:
        self.screen = pygame.display.set_mode(settings.SCREEN_SIZE, 0)
        self.set_caption()
        
        if self.role == settings.ROLE_SHOOTER:
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        
        self.create_player()
        
        self.board = Board.Board(self)
        self.screen.blit(self.board.unmasked_image, self.board.rect)
        self.screen.blit(self.board.image, self.board.rect)
        self.screen.blit(self.player.image, self.player.rect)
        
        self.zombies = [Zombie.Zombie(self)]
        for i in self.zombies:
            i.turn(*self.player.rect.center)
        
        pygame.display.update()
        self.main_loop()
        
    
    def render_zombies(self):
        """
        Determine what zombies are alive and then show them which indludes turning them towards
        the player, moving/killing them (step) and blitting.
        """
        self.zombies = [z for z in self.zombies if not z.dead]
        for z in self.zombies:
            z.turn(*self.player.rect.center)
            z.step(*self.player.rect.center)
            self.screen.blit(z.image, z.rect)
            
    
    def shoot_at_zombies(self, where):
        """
        Fire a shot at the zombies and determine whether it actually hurt one of them.
        """
        log("Shots fired at zombies: %s" % str(where))
        for z in self.zombies:
            if z.rect.collidepoint(*where):
                z.die()
        
    
    def shoot(self, where, send_event=False):
        """
        A shot happened, handle everything for it.
        """
        self.player.shoot(*where)
        if send_event:
            self.net_object.send_event(net_code.ShotFired(where))
        self.shoot_at_zombies(where)
    
    def main_loop(self):
        """
        The main loop of the game, where most of the fun happens.
        """
        counter = 0
        last_mouse_x = last_mouse_y = 0
        
        while 1:
            counter += 1
            self.clock.tick()
            
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    log("Player exited!")
                    return
                
                if self.role == settings.ROLE_SHOOTER and event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    self.shoot(mouse_pos, send_event=True)
                    
                            
            with self.event_list_lock:
                for event in self.event_list:
                    if event.msg_type == settings.NET_MSG_SHOT_FIRED:
                        self.shoot(event.where, send_event=False)
                    
                    elif event.msg_type == settings.NET_MSG_FLASHLIGHT:
                        self.board.unmask(*event.where)

                self.event_list = []
                    
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            #If the mouse moved and you are the lighter, fire a network event:
            if (self.role == settings.ROLE_LIGHTER) and (last_mouse_y != mouse_y or last_mouse_x != mouse_x):
                self.board.unmask(mouse_x, mouse_y)
                #But not too often, so that not to overwhelm the network:
                if not counter % 2:
                    self.net_object.send_event(net_code.FlashlightShine((mouse_x, mouse_y)))
            
            #Start drawing:
            self.screen.fill((0,0,0))
            self.screen.blit(self.board.unmasked_image, self.board.rect)
            
            #The shooter only sees zombies of the masked image (self.board.image) is unmasked:
            if self.role == settings.ROLE_SHOOTER:
                self.render_zombies()
                
            self.screen.blit(self.board.image, self.board.rect)
            
            if self.role == settings.ROLE_LIGHTER:
                self.render_zombies()
            
            self.player.turn(mouse_x, mouse_y)
            self.screen.blit(self.player.image, self.player.rect)
            
            if self.dirty_rects and settings.ONLY_BLIT_DIRTY_RECTS:
                pygame.display.update(self.dirty_rects)
            else:
                pygame.display.update()
            
            self.dirty_rects = []
            last_mouse_y = mouse_y
            last_mouse_x = mouse_x
            
            #print self.clock.get_fps()


    def get_player_start_position(self):
        """
        The player initial position is probably the center. Mostly?
        """
        return self.screen.get_rect().center

    def get_zombie_spawn(self):
        """
        Get a place to spawn a zombie.
        """
        return (100, 100)
    
    
    def set_caption(self):
        caption = "Byte - a zombie game (%s - %s)"
        role = "Shooter"
        if self.role == settings.ROLE_LIGHTER:
            role = "Lighter"
            
        net_role = "client"
        if self.is_server:
            net_role = "server"
        
        pygame.display.set_caption(caption % (role, net_role))
    
    

def server_start():
    utilities.log("Game started as SERVER!")
    game = Game("0.0.0.0", 12345, True, role = settings.ROLE_LIGHTER)
    game.start()
    utilities.log("Game ended!")
    
def client_start():
    utilities.log("Game started as CLIENT!")
    game = Game("localhost", 12345, False, role = settings.ROLE_SHOOTER)
    game.start()
    utilities.log("Game ended!")