import pygame as pg
import socket
from varname import nameof
from md import *
from random import randint


pg.init()
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
global screen
screen = pg.display.set_mode((screen_w, screen_h))
pg.display.set_caption("HostMenu")
clock=pg.time.Clock()
global FPS
FPS=30
global sprites
sprites=[]

global platforms
platforms=pg.sprite.Group()

def add_plat(pos, rot, scale, color):
    plat=pg.sprite.Sprite(platforms)
    plat.


is_running=True
while is_running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running=False
    pg.display.flip()
    clock.tick(FPS)
    