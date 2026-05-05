from md import *
import pygame as pg
import socket as s
from random import randint
import shelve as sh

global platforms
platforms = pg.sprite.Group()
global heroes
heroes = pg.sprite.Group()


class game:
    def __init__(self):
        pg.init()

        self.PORT = 7777
        self.HOST = "0.0.0.0"
        self.BUFFER_SIZE = 1024

        self.def_col = [255, 255, 255]
        self.def_size = [100, 100]

        self.server = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.server.bind((self.HOST, self.PORT))
        self.server.setblocking(False)

        self.screen_w = 1000
        self.screen_h = 500
        self.screen = pg.display.set_mode((self.screen_w, self.screen_h))
        pg.display.set_caption("HostMenu")
        self.clock = pg.time.Clock()
        self.FPS = 30

        self.sprites = [platforms, heroes]
        self.is_running = True
        self.def_spr = {"col": self.def_col, "size": self.def_size}

    class sprite(pg.sprite.Sprite):
        def __init__(
            self,
            sprite_group: pg.sprite.Group,
            default,
            file_name_or_col,
            size,
            center,
        ):
            self.def_col = default["col"]
            self.def_size = default["size"]
            self.colors = {
                "r": [255, 0, 0],
                "b": [0, 0, 255],
                "g": [0, 255, 0],
                "y": [255, 255, 0],
                "p": [255, 0, 255],
                "c": [0, 255, 255],
                "o": [255, 120, 0],
            }
            if size == None:
                size = self.def_size
            pg.sprite.Sprite.__init__(self)
            if isinstance(file_name_or_col, (tuple, list)):
                if len(file_name_or_col) in [3, 4]:
                    col = file_name_or_col
                else:
                    col = self.def_col
            elif isinstance(file_name_or_col, str):
                if file_name_or_col in self.colors.keys():
                    col = self.colors[file_name_or_col]
                else:
                    col = None
            else:
                col = self.def_col
            if col != None:
                self.image = pg.Surface(size=size)
                self.image.fill(col)
            else:
                try:
                    self.image = pg.transform.scale(
                        pg.image.load(file_name_or_col), size
                    )
                except:
                    self.image = pg.Surface(size=size)
                    self.image.fill(self.def_col)
            self.rect = self.image.get_rect(center=center)
            self.add(sprite_group)

        def update(self):
            pass

    class hero(sprite):
        def __init__(
            self,
            sprite_group,
            default,
            file_name_or_col,
            size,
            center,
            speed,
            weight,
            jump_power,
            friction,
        ):
            super().__init__(sprite_group, default, file_name_or_col, size, center)
            self.speed = speed
            self.weight = weight
            self.jump_power = jump_power
            self.vy = 0
            self.vx = 0
            self.ay = 0
            self.ax = 0
            self.x_axis = 0
            self.y_axis = 0
            self.is_grounded = False
            self.friction = friction
            self.collider = pg.rect.Rect(
                self.rect.left - 1,
                self.rect.top - 1,
                self.rect.width + 2,
                self.rect.height + 2,
            )
            self.collider.center = self.rect.center
            self.max_x = speed * 10
            self.max_y = weight * 20

        def update(self):
            printPlus(self.rect.center, self.vx, self.ax)
            keys = pg.key.get_pressed()
            if keys[pg.K_d]:
                self.x_axis = 1
            elif keys[pg.K_a]:
                self.x_axis = -1
            else:
                self.x_axis = 0
            if keys[pg.K_w]:
                self.y_axis = 1
            elif keys[pg.K_s]:
                self.y_axis = -1
            else:
                self.y_axis = 0

            self.ax = self.speed * self.x_axis
            if self.y_axis == -1 and not(self.is_grounded) and not(pg.sprite.spritecollideany(self, platforms)):
                self.ay = self.max_y
                self.vy=self.ay
            else:
                self.ay = self.weight

            if self.ax != 0:
                if self.vx != 0:
                    if self.vx / abs(self.vx) == self.ax / abs(self.ax):
                        self.vx += self.ax
                    else:
                        self.vx = self.ax
                else:
                    self.vx = self.ax
            else:
                if abs(self.friction) < abs(self.vx):
                    if self.vx > 0:
                        self.vx -= self.friction
                    elif self.vx < 0:
                        self.vx += self.friction
                else:
                    self.vx = 0

            if self.y_axis > 0 and self.is_grounded:
                self.vy = -self.jump_power
            else:
                self.vy += self.ay
                printPlus(self.ay)

            if abs(self.vy) > self.max_y:
                self.vy /= abs(self.vy) / self.max_y
            if abs(self.vx) > self.max_x:
                self.vx /= abs(self.vx) / self.max_x

            self.rect.x += self.vx
            self.rect.y += self.vy
            self.collider.center = self.rect.center
            collisions = []
            for sprite in platforms:
                if self.collider.colliderect(sprite.rect):
                    collisions.append(sprite)
            self.is_grounded=False
            if collisions:
                for collision in collisions:
                    if abs(abs(self.rect.centerx - collision.rect.centerx) - int(
                        (self.rect.width + collision.rect.width) / 2
                    ))<abs(abs(self.rect.centery - collision.rect.centery) - int(
                        (self.rect.height + collision.rect.height) / 2
                    )):
                        if self.rect.centerx < collision.rect.centerx:
                            if self.ax > 0:
                                self.ax = 0
                            if self.vx > 0:
                                self.vx = 0
                            self.rect.right = collision.rect.left
                        else:
                            if self.ax < 0:
                                self.ax = 0
                            if self.vx < 0:
                                self.vx = 0
                            self.rect.left = collision.rect.right
                    else:
                        if self.rect.centery < collision.rect.centery:
                            printPlus(self.ay,self.vy,brackets='""')
                            if self.ay > 0:
                                self.ay = 0
                            if self.vy > 0:
                                self.vy = 0
                            self.rect.bottom = collision.rect.top
                            if collision.rect.right>self.rect.left and collision.rect.left<self.rect.right:
                                self.is_grounded = True
                            else:
                                self.is_grounded=False
                        else:
                            if self.ay < 0:
                                self.ay = 0
                            if self.vy < 0:
                                self.vy = 0
                            self.rect.top = collision.rect.bottom
                            self.is_grounded = False
            else:
                self.is_grounded = False
                
            print(self.rect.center, "!")

    def start_game(self):
        def new_sprite(
            group: pg.sprite.Group,
            name_or_col=None,
            size=None,
            center=self.screen.get_rect().center,
        ):
            sprite=self.sprite(
                sprite_group=group,
                default=self.def_spr,
                file_name_or_col=name_or_col,
                size=size,
                center=center,
            )
            return sprite


        def new_hero(
            group: pg.sprite.Group,
            name_or_col=None,
            size=None,
            center=self.screen.get_rect().center,
            speed=2,
            weight=3,
            jump_power=24,
            friction=4,
        ):
            self.hero(
                sprite_group=group,
                default=self.def_spr,
                file_name_or_col=name_or_col,
                size=size,
                center=center,
                speed=speed,
                weight=weight,
                jump_power=jump_power,
                friction=friction,
            )

        new_hero(heroes, name_or_col="g", size=[55,100])  # игрок
        new_sprite(platforms, name_or_col=[126,126,126], size=[2000, 200], center=[500, 480])
        new_sprite(
            platforms,
            'y',
            [100, 30],
            [700, 300],
        )
        new_sprite(
            platforms,
            'p',
            [100, 30],
            [300, 250],
        )
        self.mouse=new_sprite(
            platforms,
            'b',
            [100, 30],
            [300, 250],
        )

        while self.is_running:
            self.update()

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
        self.mouse.rect.center=pg.mouse.get_pos()
        self.screen.fill([0, 0, 0])
        for sprite_group in self.sprites:
            sprite_group.draw(self.screen)
            sprite_group.update()

        pg.display.update()
        self.clock.tick(self.FPS)


g = game()
g.start_game()
