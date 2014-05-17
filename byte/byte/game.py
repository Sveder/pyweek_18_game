import sys
import data
import random
import threading

import pygame
from PyIgnition import PyIgnition

import Board
import Heart
import Bullet
import Player
import Zombie
import net_code
import settings
import utilities
from utilities import log



class Game:
    def __init__(self, host, port, is_server=True, role=settings.ROLE_LIGHTER):
        """
        Initialize the game objects and pygame.
        """
        pygame.init()
        
        self.clock = pygame.time.Clock()
        self.screen = None
        
        self.particle_frames = settings.GUN_PARTICLE_FRAMES
        self.particle_gen = None
        self.should_draw_particles = False
        
        self.zombies_killed = 0
        self.scale_zombies = 1
        
        self.buttons_pressed = (0, 0, 0)
        
        #Remote server communicates using sockets and the net code adds events to this list:
        self.event_list = []
        self.event_list_lock = threading.Lock()
        
        self.role = role
        self.host = host
        self.port = port
        self.is_server = is_server
        self.peer_connected = False
        self.should_start = False
        
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
        self.hearts = Heart.Heart(self)
        
        
        pygame.display.update()
        self.main_loop()
        self.net_object.send_event(net_code.QuitGame())
        
        self.game_over()

        log("Player exited!")
        
        self.net_object.quit_loop = True
        
    def spawn_zombie(self, loc=None, speed=None, send_event=False):
        """
        Spawn a zombie in a random location far from player. If location is given and is a two
        int tuple, the zombie will spawn there.
        """
        zombie = Zombie.Zombie(self)
        if loc:
            zombie.set_location(loc)
        
        if speed:
            zombie.set_speed(speed)
            
        zombie.turn(*self.player.rect.center)
        self.zombies.append(zombie)
        if send_event:
            self.net_object.send_event(net_code.NewZombie(zombie.rect.center, zombie.speed))
        
    
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
            if (not z.dying) and z.rect.colliderect(self.player.rect):
                self.player.hit(z)
                
            self.screen.blit(z.image, z.rect)
            
    
    def shoot_at_zombies(self, where):
        """
        Fire a shot at the zombies and determine whether it actually hurt one of them.
        """
        log("Shots fired at zombies: %s" % str(where))
        for z in self.zombies:
            if z.rect.collidepoint(*where):
                self.zombies_killed += 1
                
                if self.zombies_killed > settings.SCALE_ZOMBIES_AFTER:
                    self.zombies_killed = 0
                    self.scale_zombies += 0.2
                    
                z.die()
                
      
        
    
    def shoot(self, where, send_event=False):
        """
        A shot happened, handle everything for it.
        """
        shot_happened = self.player.shoot(*where)
        if shot_happened:
            if send_event:
                self.net_object.send_event(net_code.ShotFired(where))
            self.shoot_at_zombies(where)
        
    
    def main_loop(self):
        """
        The main loop of the game, where most of the fun happens.
        """
        counter = 0
        last_mouse_x = last_mouse_y = 0
        self.last_unmask_x = self.last_unmask_y = 0
        
        if not self.is_server:
            self.net_object.send_event(net_code.StartGame())
            
        while 1:
            counter += 1
            self.clock.tick()
            
            if self.player.life == 0:
                return
            
            with self.event_list_lock:
                if self.net_object.error:
                    log("Error in net code: %s" % self.net_object.error)
                    
                    return
                
                for event in self.event_list:
                    if event.msg_type == settings.NET_MSG_SHOT_FIRED:
                        self.shoot(event.where, send_event=False)
                    
                    elif event.msg_type == settings.NET_MSG_FLASHLIGHT:
                        self.last_unmask_x, self.last_unmask_y = event.where
                    
                    elif event.msg_type == settings.NET_MSG_QUIT:
                        return
                    
                    elif event.msg_type == settings.NET_MSG_ZOMBIE_CREATED:
                        self.spawn_zombie(event.where, event.extra, send_event=False)
                    
                    elif event.msg_type == settings.NET_MSG_RELOAD:
                        self.player.reload()
                    
                    elif event.msg_type == settings.NET_MSG_START_GAME:
                        self.should_start = True

                self.event_list = []
            
            if self.is_server and not self.should_start:
                continue
            
            if self.zombies == [] and self.net_object.is_connected:
                #Spawn a zombie for good measure:
                if self.is_server:
                    for i in xrange(int(round((self.scale_zombies - 1) * 2 ) + 1)):
                        self.spawn_zombie(send_event=True)
            
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.buttons_pressed = pygame.mouse.get_pressed()
                    
                if self.role == settings.ROLE_SHOOTER and event.type == pygame.MOUSEBUTTONUP:
                    if self.buttons_pressed[0]:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.player.rect.collidepoint(*mouse_pos):
                            self.player.joy()
                            continue
                        
                        self.shoot(mouse_pos, send_event=True)
                    
                    if self.buttons_pressed[2]:
                        self.net_object.send_event(net_code.Reload())
                        self.player.reload()
                    
                    self.buttons_pressed = (0,0,0)
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                    self.spawn_zombie(send_event=True)
                
                if event.type == settings.MUSIC_ENDED_EVENT:
                    self.board.start_music()
                
                if event.type == settings.SCHEDULE_AMBIENT_EVENT:
                    pygame.time.set_timer(settings.PLAY_AMBIENT_EVENT, random.randint(2, 30))
                
                if event.type == settings.PLAY_AMBIENT_EVENT:
                    pygame.time.set_timer(settings.PLAY_AMBIENT_EVENT, 0)
                    self.board.play_ambient()
                    
                            
            
                    
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            #Start drawing:
            self.board.reset()
            self.screen.fill((0,0,0))
            self.screen.blit(self.board.unmasked_image, self.board.rect)
            
            
            #If the mouse moved and you are the lighter, fire a network event:
            if (self.role == settings.ROLE_LIGHTER):
                self.board.unmask(mouse_x, mouse_y, is_lighter=True)
                #But not too often, so that not to overwhelm the network:
                if not (last_mouse_y != mouse_y or last_mouse_x != mouse_x) or counter % 2:
                    self.net_object.send_event(net_code.FlashlightShine((mouse_x, mouse_y)))
                    
            if self.role == settings.ROLE_SHOOTER:
                self.board.unmask(self.player.rect.center[0], self.player.rect.center[1], 200)
                self.board.unmask(self.last_unmask_x, self.last_unmask_y, 80)
            
            self.render_zombies()
            
            self.screen.blit(self.board.image, self.board.rect)
            
            self.player.turn(mouse_x, mouse_y)
            self.player.step()
            self.screen.blit(self.player.image, self.player.rect)
            
            if self.should_draw_particles:
                self.particle_gen.Update()
                self.particle_gen.Redraw()
                self.particle_frames += 1
                
                if self.particle_frames > settings.GUN_PARTICLE_FRAMES:
                    self.should_draw_particles = False
            
            self.screen.blit(self.bullets.render_bullets(self.player.bullet_count), settings.BULLET_COUNTER_LOCATION)
            if not self.player.life <= 0:
                heart_surface = self.hearts.render(self.player.life)
                where_to_put_hearts = settings.SCREEN_SIZE[0] - heart_surface.get_width() - 10
                self.screen.blit(heart_surface, (where_to_put_hearts, 10))
            
            if self.dirty_rects and settings.ONLY_BLIT_DIRTY_RECTS:
                pygame.display.update(self.dirty_rects)
            else:
                pygame.display.update()
            
            self.dirty_rects = []
            last_mouse_y = mouse_y
            last_mouse_x = mouse_x
            
            #print self.clock.get_fps()

    
    def game_over(self):
        self.screen.fill((0,0,0))
        
        skull_image, skull_rect = utilities.load_image(data.filepath(settings.SKULL_IMAGE_PATH), False)

        while 1:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return
                
            if not random.randint(0, 10) % 5:
                x = random.choice(range(self.screen.get_width()))
                y = random.choice(range(self.screen.get_height()))
                self.screen.blit(skull_image, (x, y))
                
            pygame.display.update()
    
    def get_player_start_position(self):
        """
        The player initial position is probably the center. Mostly?
        """
        return self.screen.get_rect().center
    
    
    def set_caption(self):
        caption = "8-Bit Biters - a zombie game (%s - %s)"
        role = "Shooter"
        if self.role == settings.ROLE_LIGHTER:
            role = "Lighter"
            
        net_role = "client"
        if self.is_server:
            net_role = "server"
        
        pygame.display.set_caption(caption % (role, net_role))
        
        
    def gun_particles(self, _from, direction):
        self.should_draw_particles = True
        self.particle_frames = 0
        self.particle_gen = PyIgnition.ParticleEffect(self.screen, (0, 0), settings.SCREEN_SIZE)

        particle = self.particle_gen.CreateSource(_from, initspeed = 20.0, initdirection = direction, initspeedrandrange = 0.0, initdirectionrandrange = 0.5, particlesperframe = 3, particlelife = 5, drawtype = PyIgnition.DRAWTYPE_CIRCLE, colour = (200, 0, 0), length = 2.0)
        direction = 360 - direction
        particle.SetInitDirection(1.5 + direction / 360.0 * 6.5)
        
        
        
        
    
    

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
    