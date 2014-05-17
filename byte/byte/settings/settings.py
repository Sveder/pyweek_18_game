import os

import pygame

from player_positions import *

#-------------------------------------------------------------------------------
#Debug parameters:
#-------------------------------------------------------------------------------
DEBUG = True
ONLY_BLIT_DIRTY_RECTS = False

SHOULD_LOG_TO_FILE = True
LOG_FILE = os.path.join(os.curdir, "logs", "last_run.log")
if not os.path.exists(os.path.join(os.curdir, "logs")):
    os.mkdir(os.path.join(os.curdir, "logs"))


#-------------------------------------------------------------------------------
#Game parameters:
#-------------------------------------------------------------------------------
BACKGROUND_FILL_COLOR  = (0 , 0 , 50)
SCREEN_SIZE = (800 , 600)                   #The size of the game window

MUSIC_ENDED_EVENT = pygame.USEREVENT
SCHEDULE_AMBIENT_EVENT = pygame.USEREVENT + 1
PLAY_AMBIENT_EVENT = pygame.USEREVENT + 2

PLAYER_LIFE = 3

if DEBUG:
    SHOOTER_BG_ALPHA = 30
else:
    SHOOTER_BG_ALPHA = 70
    
GUN_PARTICLE_FRAMES = 5

SIMPLE_ZOMBIE_STEP_RANGE = range(20, 35)
SCALE_ZOMBIES_AFTER = 5

ZOMBIE_SPAWN_AREA_WIDTH_PERCENT = 0.2
ZOMBIE_SPAWN_AREA_HEIGHT_PERCENT = 0.1

ROLE_NONE = 0
ROLE_SHOOTER = 1
ROLE_LIGHTER = 2

BULLET_INITIAL_COUNT = 8
BULLET_COUNTER_LOCATION = (10, 10)

SIGHT_CURSOR = (
"          XXXX          ",
"         X XX X         ",
"        X  XX  X        ",
"       X   XX   X       ",
"      X    XX    X      ",
"     X     XX     X     ",
"    X      XX      X    ",
"   X       XX       X   ",
"  X        XX        X  ",
" X         XX         X ",
"XXXX XX XXXXXXXX XX XXXX",
"XXXX XX XXXXXXXX XX XXXX",
" X         XX         X ",
"  X        XX        X  ",
"   X       XX       X   ",
"    X      XX      X    ",
"     X     XX     X     ",
"      X    XX    X      ",
"       X   XX   X       ",
"        X  XX  X        ",
"         X XX X         ",
"          XXXX          ",
"           XX           ",
"                        ",)



#-------------------------------------------------------------------------------
#File/Path parameters:
#-------------------------------------------------------------------------------
IMAGE_FOLDER = "images"
SOUND_FOLDER = "sounds"

BULLET_IMAGE_PATH = os.path.join(IMAGE_FOLDER, "bullet.png")
HEART_IMAGE_PATH = os.path.join(IMAGE_FOLDER, "heart.png")
SKULL_IMAGE_PATH = os.path.join(IMAGE_FOLDER, "skull.png")

PLAYER_IMAGE_PATH_FORMAT = os.path.join(IMAGE_FOLDER, "player", "player_small_%s.png")


PLAYER_SHOT_SOUND = os.path.join(SOUND_FOLDER, "shot.ogg")
PLAYER_HAPPY_SOUND = os.path.join(SOUND_FOLDER, "happy_happy_joy_joy.ogg")
PLAYER_EMPTY_SHOT_SOUND = os.path.join(SOUND_FOLDER, "empty_shot.ogg")
PLAYER_RELOAD_SOUND = os.path.join(SOUND_FOLDER, "reload.ogg")
PLAYER_DEATH_SOUND = os.path.join(SOUND_FOLDER, "death.ogg")
PLAYER_HIT_SOUND = os.path.join(SOUND_FOLDER, "player_hit.ogg")

MASKED_BG_IMAGE_PATH = os.path.join(IMAGE_FOLDER, "masked_bg.jpg")
UNMASKED_BG_IMAGE_PATH = os.path.join(IMAGE_FOLDER, "unmasked_bg.jpg")

ZOMBIE_FOLDER = os.path.join(IMAGE_FOLDER, "zombies")

SIMPLE_ZOMBIE_FORMATS = [
    os.path.join(ZOMBIE_FOLDER, "simple_1", "simple_%s.png"),
    os.path.join(ZOMBIE_FOLDER, "simple_2", "simple2_%s.png"),
    os.path.join(ZOMBIE_FOLDER, "simple_3", "simple3_%s.png"),
    os.path.join(ZOMBIE_FOLDER, "simple_4", "simple4_%s.png"),
]

ZOMBIE_SOUND_FOLDER = os.path.join(SOUND_FOLDER, "zombie")
AMBIENT_ZOMBIE_SOUND = os.path.join(ZOMBIE_SOUND_FOLDER, "ambient_zombie_call.ogg")
ZOMBIE_SPAWN_SOUND = os.path.join(ZOMBIE_SOUND_FOLDER, "far_away_zombie.ogg")
ZOMBIE_DEATH_SOUND = os.path.join(ZOMBIE_SOUND_FOLDER, "death.ogg")


MUSIC_FOLDER = os.path.join(SOUND_FOLDER, "music")
MUSIC_TRACKS = [
    os.path.join(MUSIC_FOLDER, "music_1.ogg"),
    os.path.join(MUSIC_FOLDER, "music_2.ogg"),
]

AMBIENT_SOUNDS = [
    AMBIENT_ZOMBIE_SOUND,
]



#-------------------------------------------------------------------------------
#Net parameters:
#-------------------------------------------------------------------------------

NET_MAGIC_HEADER_SERVER = "server_header0.2>>>"
NET_MAGIC_HEADER_CLIENT = "client_header0.2>>>"

NET_MSG_ZOMBIE_CREATED = 1
NET_MSG_FLASHLIGHT = 2
NET_MSG_SHOT_FIRED = 3
NET_MSG_QUIT = 4
NET_MSG_RELOAD = 5
NET_MSG_START_GAME = 6