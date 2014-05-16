import os
import math
import time
import select
import socket
import struct

import pygame

import atexit
import settings
from utilities import log

#Messages that are passed through the net and some utility classes to make it easier to instantiate them
class Message:
    def __init__(self, msg_type=None, where=(0, 0)):
        self.msg_type = msg_type
        self.where = where
    
    def __repr__(self):
        return "Message %s at %s." % (self.msg_type, self.where)
    

class FlashlightShine(Message):
    def __init__(self, where):
        Message.__init__(self, settings.NET_MSG_FLASHLIGHT, where)
        
class ShotFired(Message):
    def __init__(self, where):
        Message.__init__(self, settings.NET_MSG_SHOT_FIRED, where)

class NewZombie(Message):
    def __init__(self, where):
        Message.__init__(self, settings.NET_MSG_ZOMBIE_CREATED, where)
        
class QuitGame(Message):
    def __init__(self):
        Message.__init__(self, settings.NET_MSG_QUIT)
    


class NetBase:
    """
    Base class for client and server, mostly controls the receiving and sending of messages, while each individual
    client/server controls the handshake.
    """
    def __init__(self):
        self.is_connected = False
        self.conn = None
        self.game = None
        self.quit_loop = False
        self.error = None
    

    def send_event(self, event):
        """
        Send the given event if the socket is connected.
        """
        if not self.is_connected or not self.conn:
            return
        
        data = struct.pack("<iii", event.msg_type, event.where[0], event.where[1])
        self.conn.send(data)
    
    
    def recv_event_loop(self):
        """
        Wait for incoming events and add them to the event queue until the loop should be quit.
        """
        if not self.is_connected or not self.conn:
            raise Exception("Trying to enter game NET loop while not connected or no self.conn.")
        
        while not self.quit_loop:
            try:
                self.recv_event()
            except Exception, e:
                import traceback; traceback.print_exc()
                log("Exception in recv loop.", True)
        
    
    def recv_event(self):
        #Block for a short time while waiting for incoming event:
        ready = select.select([self.conn], [], [], 0.1) 
        if ready[0]:
            data = self.conn.recv(4096)
    
            for message_start in xrange(0, len(data), struct.calcsize("<iii")):
                message = data[message_start:12]
                if not message: continue
                
                #Discard fragmented and unloadable messages:
                try:
                    message = struct.unpack("<iii", message)
                except:
                    continue
                
                #Recreate the Message object:
                msg_object = Message(message[0], (message[1], message[2]))
                log("Received message from remote: %s" % msg_object)
                
                self._add_to_game_queue(msg_object)
        
        #Don't run on 100% cpu. Probably redundant as select does the same, but no time to research it:
        time.sleep(0)
    
    
    def _add_to_game_queue(self, message):
        """
        Add the event given to the game event queue in a thread safe manner.
        """
        if not self.game:
            return
        
        with self.game.event_list_lock:
            self.game.event_list.append(message)



class Server(NetBase):
    def start(self, game):
        self.game = game
        log("Starting server on port: %s" % self.game.port)
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.game.host, self.game.port))
        s.listen(1)
        
        conn, addr = s.accept()
        self.is_connected = True
        self.conn = conn
        
        #Send header and wait for response:
        conn.send(settings.NET_MAGIC_HEADER_SERVER)
        data = conn.recv(len(settings.NET_MAGIC_HEADER_CLIENT))
        
        if data != settings.NET_MAGIC_HEADER_CLIENT:
            log("Server recieved wrong header: %s" % data)
            raise Excpetion()
        
        role = conn.recv(1)
        role = int(role)
        if role not in [settings.ROLE_LIGHTER, settings.ROLE_SHOOTER]:
            log("Server recieved bad role: %s" % role)
            raise Excpetion()
        
        if role == self.game.role:
            log("A user with the same role has connected.")
            self.error = "A user with the same role has connected."
            return
        
        self.recv_event_loop()
    
    
class Client(NetBase):
    def connect(self, game):
        self.game = game
        log("Connecting to: %s:%s" % (self.game.host, self.game.port))
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.game.host, self.game.port))
        self.is_connected = True
        
        header = s.recv(len(settings.NET_MAGIC_HEADER_SERVER))
        if header != settings.NET_MAGIC_HEADER_SERVER:
            log("Client recieved wrong header: %s" % header)
            raise Excpetion()
        
        s.send(settings.NET_MAGIC_HEADER_CLIENT)
        s.send("%s" % self.game.role)
        self.conn = s
        
        self.recv_event_loop()

