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
        self.FPS = 60

        self.sprites = pg.sprite.Group()
        self.sprite_groups = [platforms, heroes]
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
            all_sprites: pg.sprite.Group,
        ):
            self.old_rect=self.rect
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
            self.add(all_sprites)

        def update(self):
            self.old_rect = self.rect

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
            all_sprites,
        ):
            super().__init__(
                sprite_group, default, file_name_or_col, size, center, all_sprites
            )
            self.speed = speed
            self.weight = weight
            self.vy = 0
            self.vx = 0
            self.ay = 0
            self.ax = 0
            self.x_axis = 0
            self.y_axis = 0
            self.is_grounded = False
            self.friction = friction
            self.jump_power = jump_power
            self.max_x = self.speed * 10
            self.max_y = self.weight * 10
            self.can_collision = []

        def update(self):
            super().update()
            keys = pg.key.get_pressed()
            self.ax = self.speed * (0 + int(keys[pg.K_d]) - int(keys[pg.K_a]))
            if keys[pg.K_s] and not (self.is_grounded):
                self.ay = self.max_y
                self.vy = self.ay
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

            if abs(self.vx) > self.max_x:
                self.vx /= abs(self.vx) / self.max_x

            if not (keys[pg.K_s]) and self.is_grounded and keys[pg.K_w]:
                self.ay = -self.jump_power
            self.vy += self.ay

            if abs(self.vy) > self.max_y:
                self.vy /= abs(self.vy) / self.max_y

            self.is_grounded = False

            self.rect.y += self.vy

            collisions = 1
            global old_colls
            old_colls = []
            while collisions:
                collisions = pg.sprite.spritecollide(self, platforms, False)
                if collisions:
                    if collisions[0] not in old_colls:
                        coll = collisions[0]
                        old_colls.append(coll)
                        if (
                            self.old_rect.centery - self.rect.centery
                            < coll.old_rect.centery - coll.rect.centery
                        ):
                            if not (coll.is_one_way):
                                self.rect.top = coll.rect.bottom
                                self.vy = 0
                        elif (
                            self.old_rect.centery - self.rect.centery
                            > coll.old_rect.centery - coll.rect.centery
                        ):
                            if (
                                not (coll.is_one_way)
                                or self.rect.bottom - coll.rect.top <= self.vy
                            ):
                                self.rect.bottom = coll.rect.top
                                self.ay = 0
                                self.vy = 0
                                self.is_grounded = True
                    else:
                        break

            self.rect.x += self.vx

            collisions = 1
            old_colls = []
            while collisions:
                collisions = pg.sprite.spritecollide(self, platforms, False)
                if collisions:
                    index = randint(0, len(collisions) - 1)
                    if collisions[index] not in old_colls:
                        coll = collisions[index]
                        old_colls.append(coll)
                        if not (coll.is_one_way):
                            if self.vx < 0:
                                self.rect.left = coll.rect.right
                                self.vx = 0
                                self.ax = 0
                            elif self.vx > 0:
                                self.rect.right = coll.rect.left
                                self.vx = 0
                                self.ax = 0
                    else:
                        break

    class platform(sprite):
        def __init__(
            self,
            sprite_group,
            default,
            file_name_or_col,
            size,
            center,
            is_one_way: bool,
            all_sprites,
        ):
            super().__init__(
                sprite_group, default, file_name_or_col, size, center, all_sprites
            )
            self.is_one_way = is_one_way
            self.is_render=False
            self.rend_col=self.def_col

        def update(self):
            return super().update()

    def start_game(self):
        def new_plat(
            group: pg.sprite.Group,
            name_or_col=None,
            size=None,
            center=self.screen.get_rect().center,
            is_one_way=False,
        ):
            sprite = self.platform(
                sprite_group=group,
                default=self.def_spr,
                file_name_or_col=name_or_col,
                size=size,
                center=center,
                is_one_way=is_one_way,
                all_sprites=self.sprites,
            )
            return sprite

        def new_hero(
            group: pg.sprite.Group,
            name_or_col=None,
            size=None,
            center=self.screen.get_rect().center,
            speed=1,
            weight=2,
            friction=2,
            jump_power=20,
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
                all_sprites=self.sprites,
            )

        new_hero(heroes, name_or_col="g", size=[40, 70])  # игрок
        new_plat(
            platforms,
            name_or_col=[126, 126, 126],
            size=[2000, 200],
            center=[500, 480],
        )
        new_plat(platforms, "y", [65, 25], [700, 290], is_one_way=True)
        new_plat(
            platforms,
            "p",
            [100, 30],
            [450, 250],
            is_one_way=False,
        )
        new_plat(
            platforms,
            [126, 126, 126],
            [100, 1000],
            [0, 250],
        )
        new_plat(
            platforms,
            [126, 126, 126],
            [100, 1000],
            [self.screen_w, 250],
        )

        while self.is_running:
            self.update()

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
        self.screen.fill([0, 0, 0])
        for sprite_group in self.sprite_groups:
            sprite_group.draw(self.screen)
            sprite_group.update()

        pg.display.update()
        self.clock.tick(self.FPS)


g = game()
g.start_game()
