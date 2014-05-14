import os
import json
import math
import time
import select
import socket

import pygame

import atexit
import settings
from utilities import log


class Message:
    def __init__(self, msg_type=None, where=None):
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
    


class NetBase:
    """
    Base class for client and server, mostly controls the receiving and sending of messages, while each individual
    client/server controls the handshake.
    """
    def __init__(self):
        self.is_connected = False
        self.conn = None
        self.game = None
    
    def send_event(self, event):
        """
        Send the given event if the socket is connected.
        """
        if not self.is_connected or not self.conn:
            return
        
        data = json.dumps(event.__dict__) #Can't dump arbitrary python objects... :(
        self.conn.send(data)
    
    
    def recv_event_loop(self):
        """
        Wait for incoming events and add them to the event queue.
        """
        if not self.is_connected or not self.conn:
            raise Exception("Trying to enter game NET loop while not connected or no self.conn.")
        
        while 1:
            ready = select.select([self.conn], [], [], 0.1) #Wait 0.1 seconds.
            if ready[0]:
                data = self.conn.recv(1024)
                message = json.loads(data)
                msg_object = Message(*message)
                msg_object.__dict__ = message
                
                log("Received message from remote: %s" % msg_object)
                
                self._add_to_game_queue(msg_object)
            
            time.sleep(0)
    
    
    def _add_to_game_queue(self, message):
        """
        Add the event given to the game event queue in a thread safe manner.
        """
        if not self.game:
            return
        
        with self.game.event_list_lock:
            self.game.event_list.append(message)

        log("Added message to game queue: %s." % message)

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
            raise Exception()
        
        self.recv_event_loop()
    
    
            
        
class Client(NetBase):
    def connect(self, game):
        self.game = game
        log("Connecting to: %s:%s" % (self.game.host, self.game.port))
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s.setblocking(0)
        s.connect((self.game.host, self.game.port))
        self.is_connected = True
        header = s.recv(len(settings.NET_MAGIC_HEADER_SERVER))
        if header != settings.NET_MAGIC_HEADER_SERVER:
            print "omg fail~!!!@!#" * 400
            log("Client recieved wrong header: %s" % header)
            raise Excpetion()
        
        s.send(settings.NET_MAGIC_HEADER_CLIENT)
        s.send("%s" % self.game.role)
        self.conn = s
        
        self.recv_event_loop()

