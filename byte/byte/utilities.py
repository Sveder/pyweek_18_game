import os
import math

import pygame

import atexit
import settings
import traceback

g_open_log_file = None

def load_image(path, convert=True):
    """
    Loads the image and returns it and it's rect.
    """
    #Check if the file exists:
    if not os.path.isfile(path):
        raise ValueError("Image requested to load doesn't exist: %s" % path)
    
    #Load the image and return the needed values:
    image = pygame.image.load(path)
    if convert:
        image = image.convert()
        
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
            


class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error, message:
            print 'Unable to load spritesheet image:', filename
            raise SystemExit, message
    
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]
    
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)