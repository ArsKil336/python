import pygame
import socket
from varname import nameof
from md import *
from random import randint

class aspect:
    def __init__(self, name, start=None, update=None, vars=None):
        self.name=name
        self.start=start
        self.update=update
        self.vars=vars

class object:
    def __init__(self, *aspects):
        aspects=list(aspects)
        self.aspects=dict()
        for this_aspect in args:
            this_aspect:aspect
            self.aspects[this_aspect.name]=this_aspect
    def update(self):
        



PORT = 7777
HOST = "0.0.0.0"
BUFFER_SIZE = 1024

    # Создание UDP-сокета
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Привязка к адресу и порту
server.bind((HOST, PORT))
server.setblocking(False)

screen_w = 160*4
screen_h = 90*4
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("HostMenu")
clock=pygame.time.Clock()
global objects
objects=[]

is_running=True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running=False
    