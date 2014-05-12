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


#-------------------------------------------------------------------------------
#File/Path parameters:
#-------------------------------------------------------------------------------
IMAGE_FOLDER = "images"

PLAYER_IMAGE_PATH_FORMAT = os.path.join(IMAGE_FOLDER, "player", "player_%s.png")

MASKED_BG_IMAGE_PATH = os.path.join(IMAGE_FOLDER, "masked_bg.jpg")
UNMASKED_BG_IMAGE_PATH = os.path.join(IMAGE_FOLDER, "unmasked_bg.jpg")
