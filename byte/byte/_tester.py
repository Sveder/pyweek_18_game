###import game
###
###game.client_start()

##import settings
##import pygame
##pygame.init()
##
###Load music:
##tracks = []
##cur_track = 0
##for track in settings.MUSIC_TRACKS:
##    sound = pygame.mixer.Sound(track)
##    tracks.append(sound)
##
##
##
##def start_music():
##    global cur_track, tracks
##    channel = tracks[cur_track].play()
##    
##    
##    cur_track += 1
##    cur_track %= len(tracks)
##    
##    
##start_music()
##
##
##while 1:
##    import time
##    time.sleep(0)

from PyIgnition import PyIgnition
print dir(PyIgnition)