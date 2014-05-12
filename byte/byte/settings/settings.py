import os

#-------------------------------------------------------------------------------
#Debug parameters:
#-------------------------------------------------------------------------------
DEBUG = True

SHOULD_LOG_TO_FILE = True
LOG_FILE = os.path.join(os.curdir, "logs", "last_run.log")
if not os.path.exists(os.path.join(os.curdir, "logs")):
    os.mkdir(os.path.join(os.curdir, "logs"))


#-------------------------------------------------------------------------------
#Game parameters:
#-------------------------------------------------------------------------------
BACKGROUND_FILL_COLOR  = (0 , 0 , 50)
SCREEN_SIZE = (800 , 600)                   #The size of the game window



#-------------------------------------------------------------------------------
#File/Path parameters:
#-------------------------------------------------------------------------------
IMAGE_FOLDER = "images"

PLAYER_IMAGE_PATH_FORMAT = os.path.join(IMAGE_FOLDER, "player", "player_%s.png")
