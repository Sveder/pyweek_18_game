import os

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


if DEBUG:
    SHOOTER_BG_ALPHA = 30
else:
    SHOOTER_BG_ALPHA = 70
    

SIMPLE_ZOMBIE_STEP = 1

ZOMBIE_SPAWN_AREA_WIDTH_PERCENT = 0.3
ZOMBIE_SPAWN_AREA_HEIGHT_PERCENT = 0.2

ROLE_NONE = 0
ROLE_SHOOTER = 1
ROLE_LIGHTER = 2

BULLET_INITIAL_COUNT = 8
BULLET_COUNTER_LOCATION = (10, 10)


#-------------------------------------------------------------------------------
#File/Path parameters:
#-------------------------------------------------------------------------------
IMAGE_FOLDER = "images"
SOUND_FOLDER = "sounds"

BULLET_IMAGE_PATH = os.path.join(IMAGE_FOLDER, "bullet.png")

PLAYER_IMAGE_PATH_FORMAT = os.path.join(IMAGE_FOLDER, "player", "player_%s.png")
PLAYER_SHOT_SOUND = os.path.join(SOUND_FOLDER, "shot.mp3")

MASKED_BG_IMAGE_PATH = os.path.join(IMAGE_FOLDER, "masked_bg.jpg")
UNMASKED_BG_IMAGE_PATH = os.path.join(IMAGE_FOLDER, "unmasked_bg.jpg")

ZOMBIE_FOLDER = os.path.join(IMAGE_FOLDER, "zombies")

SIMPLE_ZOMBIE_FOLDER = os.path.join(ZOMBIE_FOLDER, "simple")
SIMPLE_ZOMBIE_PATH_FORMAT = os.path.join(SIMPLE_ZOMBIE_FOLDER, "simple_%s.png")


#-------------------------------------------------------------------------------
#Net parameters:
#-------------------------------------------------------------------------------

NET_MAGIC_HEADER_SERVER = "server_header0.0>>>"
NET_MAGIC_HEADER_CLIENT = "client_header0.0>>>"

NET_MSG_ZOMBIE_CREATED = 1
NET_MSG_FLASHLIGHT = 2
NET_MSG_SHOT_FIRED = 3
NET_MSG_QUIT = 4




