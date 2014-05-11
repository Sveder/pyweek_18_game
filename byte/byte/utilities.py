import os

import pygame

import atexit
import settings
import traceback

g_open_log_file = None

def load_image(path):
    """
    Loads the image and returns it and it's rect.
    """
    #Check if the file exists:
    if not os.path.isfile(path):
        raise ValueError("Image requested to load doesn't exist: %s" % path)
    
    #Load the image and return the needed values:
    image = pygame.image.load(path)
    rect = image.get_rect()
    return image , rect


###def resize_image(path , x , y):
###    """
###    Resizes the image in the path path to the specified size
###    """
###    image_obj = Image.open(path)
###    resized_image = image_obj.resize((x , y))
###    resized_image.save(path)


def log(message, trace=False):
    """
    Log the message given wherever you can.
    If trace is true also add the stack trace.
    """
    if trace:
        trace_string = "".join(traceback.format_stack())
        message = "%s\nStack trace:\n%s\n" % (message, trace_string)
        
    if settings.DEBUG:
        print message
    
    if settings.SHOULD_LOG_TO_FILE:
        global g_open_log_file
        if not g_open_log_file:
            g_open_log_file = open(settings.LOG_FILE , "w")
            #Make sure the file is closed on exit:
            atexit.register(g_open_log_file.close)
            
        g_open_log_file.write(message + "\n")
            
