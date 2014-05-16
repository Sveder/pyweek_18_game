import sys
import data
import random
import threading

import pygame

import Board
import Bullet
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
        self.peer_connected = False
        
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
            cursor = pygame.cursors.compile(settings.SIGHT_CURSOR)
            pygame.mouse.set_cursor((24, 24), (12, 12), *cursor)
        else:
            pygame.mouse.set_visible(False)
        
        self.create_player()
        
        self.board = Board.Board(self)
        self.screen.blit(self.board.unmasked_image, self.board.rect)
        self.screen.blit(self.board.image, self.board.rect)
        self.screen.blit(self.player.image, self.player.rect)
        
        self.zombies = []
        
        self.bullets = Bullet.Bullet(self)
        
        
        pygame.display.update()
        self.main_loop()
        
        self.net_object.send_event(net_code.QuitGame())
        log("Player exited!")
        
        self.net_object.quit_loop = True
        
    def spawn_zombie(self, loc=None, send_event=False):
        """
        Spawn a zombie in a random location far from player. If location is given and is a two
        int tuple, the zombie will spawn there.
        """
        zombie = Zombie.Zombie(self)
        if loc:
            zombie.set_location(loc)
        zombie.turn(*self.player.rect.center)
        self.zombies.append(zombie)
        if send_event:
            self.net_object.send_event(net_code.NewZombie(zombie.rect.center))
        
    
    def get_zombie_spawn(self):
        """
        Get a place to spawn a zombie.
        """
        width_lower_range = range(0, int(settings.ZOMBIE_SPAWN_AREA_WIDTH_PERCENT * self.board.rect.width))
        width_higher_range = range(self.board.rect.width - int(settings.ZOMBIE_SPAWN_AREA_WIDTH_PERCENT * self.board.rect.width), self.board.rect.width)
    
        height_lower_range = range(0, int(settings.ZOMBIE_SPAWN_AREA_HEIGHT_PERCENT * self.board.rect.height))
        height_higher_range = range(self.board.rect.height - int(settings.ZOMBIE_SPAWN_AREA_HEIGHT_PERCENT * self.board.rect.height), self.board.rect.height)

        return random.choice(width_higher_range + width_lower_range), random.choice(height_lower_range + height_higher_range)
        
    
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
        last_unmask_x = last_unmask_y = 0
        
        while 1:
            counter += 1
            self.clock.tick()
            
            with self.event_list_lock:
                if self.net_object.error:
                    log("Error in net code: %s" % self.net_object.error)
                    
                    return
                
                for event in self.event_list:
                    if event.msg_type == settings.NET_MSG_SHOT_FIRED:
                        self.shoot(event.where, send_event=False)
                    
                    elif event.msg_type == settings.NET_MSG_FLASHLIGHT:
                        last_unmask_x, last_unmask_y = event.where
                    
                    elif event.msg_type == settings.NET_MSG_QUIT:
                        return
                    
                    elif event.msg_type == settings.NET_MSG_ZOMBIE_CREATED:
                        self.spawn_zombie(event.where, send_event=False)

                self.event_list = []
                
            if not self.net_object.is_connected:
                continue
            
            if self.zombies == []:
                #Spawn a zombie for good measure:
                if self.role == settings.ROLE_LIGHTER:
                    self.spawn_zombie(send_event=True)
            
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return
                
                if self.role == settings.ROLE_SHOOTER and event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    self.shoot(mouse_pos, send_event=True)
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                    self.spawn_zombie(send_event=True)
                
                if event.type == pygame.USEREVENT:
                    self.board.start_music()
                    
                            
            
                    
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            #If the mouse moved and you are the lighter, fire a network event:
            if (self.role == settings.ROLE_LIGHTER) and (last_mouse_y != mouse_y or last_mouse_x != mouse_x):
                self.board.unmask(mouse_x, mouse_y)
                #But not too often, so that not to overwhelm the network:
                if not counter % 2:
                    self.net_object.send_event(net_code.FlashlightShine((mouse_x, mouse_y)))
            
            elif self.role == settings.ROLE_SHOOTER:
                self.board.unmask(last_unmask_x, last_unmask_y)
            
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
            
            self.screen.blit(self.bullets.render_bullets(self.player.bullet_count), settings.BULLET_COUNTER_LOCATION)
            
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
    
def start():
    log("Game started with the following args: %s" % str(sys.argv[1:]))
    is_server, role_s, host, port = sys.argv[1:]
    
    role = settings.ROLE_LIGHTER
    if role_s == "shooter":
        role = settings.ROLE_SHOOTER
    
    port = int(port)
    
    if is_server == "y":
        utilities.log("Game started as SERVER!")
        game = Game(host, port, True, role)
    else:
        utilities.log("Game started as CLIENT!")
        game = Game(host, port, False, role)
        
    game.start()
    