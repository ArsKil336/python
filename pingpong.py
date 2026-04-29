import pygame, socket, os, time
from random import randint
from md import rangeList, ListMagic, ListToNums


def null():
    pass


def text_to_other(text: str):
    if type(text) is str:
        if text[0] in "([" and text[-1] in ")]":
            l = []
            l.extend(text)
            del l[0]
            del l[-1]
            text = "".join(l)
            text = text.split(", ")
            for i in range(len(text)):
                text[i] = text_to_other(text[i])
        elif text == "False":
            text = False
        elif text == "True":
            text = True
        else:
            try:
                text = float(text)
            except ValueError:
                pass
            try:
                if text == int(text):
                    text = int(text)
            except ValueError:
                pass
    return text


def to_dict(text: str):
    text = "".join("".join(text.split("{")).split("}"))
    text1 = ""
    is_el = False
    for i in text:
        if i == ",":
            if not (is_el):
                text1 += ";"
            else:
                text1 += ","
        else:
            text1 += i
            if i in "[(":
                is_el = True
            elif i in ")]":
                is_el = False
    text = text1
    text = text.split("; ")
    new_dict = dict()
    for key_item in text:
        key, item = key_item.split(": ")
        key = "".join(key.split("'"))
        item = "".join(item.split("'"))
        item = text_to_other(item)
        new_dict[key] = item
    return new_dict


def get_p_len(SCREEN_HEIGHT):
    return int(3 / 8 * (SCREEN_HEIGHT - 2))


try:
    with open("data.txt", "r") as file:
        settings = to_dict(file.read())
except FileNotFoundError:
    settings = {
        "version": 1,
        "default_color": "RANDOM",
        "nickname": "Player_" + str(randint(2000, 7000)),
        "bg_color": [0, 0, 0],
        "def_fps": 60,
        "block_scale": 50,
        "SCREEN_WIDTH_GAME": 16,
        "SCREEN_HEIGHT_GAME": 10,
        "ending_time": 0,
    }
    with open("data.txt", "w") as file:
        file.write(str(settings))
global version
version = str(settings.get("version"))
CHEATS = bool(settings.get("CHEATS"))
if CHEATS == None:
    CHEATS = False
scale_x_off = 250
scale_x_on = 250 * 1.2
scale_y_off = 150
scale_y_on = 150 * 1.2
pudding = 250 / 5
server = None
pygame.init()
n = [0, {"text_error": f"версия: {version}"}]
BG_COLOR = settings.get("bg_color")
color = settings.get("default_color")
if color == "RANDOM":
    try:
        with open("colors.txt", "r") as file:
            colors = file.read().split("\n")
            print(colors)
            color = text_to_other(colors[randint(0, len(colors) - 1)])
    except:
        colors = "[6, 90, 117]\n[50, 120, 255]\n[255, 120, 50]\n[32, 128, 0]\n[255, 255, 255]\n[198, 53, 45]\n[228, 80, 141]"
        with open("colors.txt", "w") as file:
            file.write(colors)
        color = colors[randint(0, len(colors) - 1)]
end_time = settings.get("ending_time")
def_fps = settings.get("def_fps")
block_scale = settings.get("block_scale")
SCREEN_WIDTH = settings.get("SCREEN_WIDTH_GAME")
SCREEN_HEIGHT = settings.get("SCREEN_HEIGHT_GAME")
nickname = str(settings.get("nickname"))
global all_settings
all_settings = {
    "nickname": nickname,
    "block_scale": block_scale,
    "def_fps": def_fps,
    "server": server,
    "SCREEN_WIDTH": SCREEN_WIDTH,
    "SCREEN_HEIGHT": SCREEN_HEIGHT,
}
clock = pygame.time.Clock()
pygame.font.init()


class Text:
    def __init__(
        self,
        screen: pygame.Surface,
        text: str = "text",
        size: int = 40,
        color: tuple = color,
    ):
        self.font = pygame.font.Font(None, size)
        self.text = text
        self.size = size
        self.color = color
        self.text_rect = self.font.render(self.text, False, color)
        self.rect = self.text_rect.get_rect()
        self.width = self.rect.left - self.rect.right
        self.height = self.rect.bottom - self.rect.top
        self.screen = screen

    def set_pos(self, position=(0, 0)):
        self.rect.centerx, self.rect.centery = position

    def set_text(self, text: str, center_pos="center"):
        self.text = text
        self.text_rect = self.font.render(text, False, self.color)
        if center_pos == "center":
            x = self.rect.centerx
        self.rect.width = self.text_rect.get_rect().width
        self.rect.height = self.text_rect.get_rect().height
        if center_pos == "center":
            self.rect.centerx = x
        self.width = self.rect.width
        self.height = self.rect.height

    def draw(self):
        self.screen.blit(self.text_rect, self.rect)


class Button:
    def __init__(
        self,
        button_def,
        img_off: pygame.Surface,
        img_on: pygame.Surface,
        position,
        screen: pygame.Surface,
        size_off=1,
        size_on=1,
    ):
        self.screen = screen
        self.img_off = img_off
        self.img_on = img_on
        self.rect = self.img_off.get_rect()
        self.rect.inflate_ip(0, 0)
        self.set_position(position)
        self.angle = 0
        self.button_def = button_def
        self.is_focus = False
        self.size_off = ListToNums(
            ListMagic((img_off.get_rect().width, img_off.get_rect().height), size_off)
        )
        self.size_on = ListToNums(
            ListMagic((img_on.get_rect().width, img_on.get_rect().height), size_on)
        )

    def img(self):
        self.is_focus = self.rect.collidepoint(pygame.mouse.get_pos())
        if self.is_focus:
            self.rotated_image = pygame.transform.rotate(self.img_on, self.angle)
            self.rotated_image = pygame.transform.scale(
                self.rotated_image, self.size_on
            )
        else:
            self.rotated_image = pygame.transform.rotate(self.img_off, self.angle)
            self.rotated_image = pygame.transform.scale(
                self.rotated_image, self.size_off
            )
        self.rect = self.rotated_image.get_rect(center=self.rect.center)

    def draw(self):
        self.screen.blit(self.rotated_image, self.rect)

    def set_position(self, position=(0, 0)):
        self.rect.center = position

    def set_position_xy(self, position_x: int = 0, position_y: int = 0):
        self.rect.left, self.rect.centery = (position_x, position_y)

    def click(self):
        return self.button_def()


class Input:
    def __init__(
        self,
        count,
        only_nums,
        letter_size,
        screen: pygame.Surface,
        FPS: int,
        start_text="",
        color=color,
        pos=(0, 0),
        interval_anim: float = 0.5,
    ):
        self.is_stick = True
        self.color = color
        self.stick = pygame.Surface((int(letter_size / 20), int(letter_size / 2)))
        self.FPS = FPS
        self.count = count
        self.only_nums = only_nums
        self.letter_size = letter_size
        self.is_pressed = pygame.key.get_pressed()
        self.symbols = "abcdefghijklmnopqrstuvwxyz"
        self.range_ind = rangeList(48, 57)
        self.range_ind.append(45)
        self.range_ind.append(8)
        self.text = ""
        self.screen = screen
        self.text_obj = Text(screen, self.text, letter_size)
        self.add(start_text)
        if not (self.only_nums):
            self.range_ind += rangeList(97, 122)
        self.anim_count = 0
        self.anim = interval_anim * FPS
        self.text_obj.set_pos(pos)

    def update(self):
        current_key = pygame.key.get_pressed()
        self.anim_count += 1
        if self.anim_count >= self.anim:
            self.anim_count = 0
            self.is_stick = not (self.is_stick)
        for key in self.range_ind:
            if current_key[key]:
                if not (self.is_pressed[key]):
                    if key < 58:
                        if key != 45:
                            if key != 8:
                                self.add(key - 48)
                            else:
                                self.add(-1)
                        else:
                            if (
                                current_key[pygame.K_LSHIFT]
                                or current_key[pygame.K_RSHIFT]
                            ):
                                self.add("_")
                            else:
                                self.add("-")
                    else:
                        if current_key[pygame.K_LSHIFT] or current_key[pygame.K_RSHIFT]:
                            self.add(self.symbols.upper()[key - 97])
                        else:
                            self.add(self.symbols[key - 97])
        self.is_pressed = current_key

        self.draw()

    def draw(self):
        self.text_obj.draw()
        if self.is_stick:
            self.stick.fill(color=self.color)
            self.screen.blit(
                self.stick,
                (
                    self.text_obj.rect.right,
                    self.text_obj.rect.centery
                    - int(self.stick.get_rect().height / 2)
                    - int(self.text_obj.rect.height / 20),
                ),
            )

    def add(self, symbol):
        self.anim_count = 0
        self.is_stick = True
        if symbol != -1:
            if self.only_nums:
                try:
                    symbol = str(int(symbol))
                except ValueError:
                    symbol = ""
            self.text += str(symbol)
            if len(self.text) > self.count:
                self.text = self.text[: self.count]
        else:
            if len(self.text) > 0:
                self.text = self.text[: len(self.text) - 1]
        self.text_obj.set_text(self.text, "left")

    def set_pos(self, pos: tuple = (0, 0)):
        if type(pos) is tuple or type(pos) is list:
            if len(pos) > 1:
                self.pos = pos[:2]

    def set_posxy(self, posx, posy):
        self.pos = (posx, posy)


def join_input_menu(args: dict = dict(), y: int = None, FPS=30):
    screen_w = 800
    screen_h = 400
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("JoinMenu")
    if "text_error" in args.keys():
        text_error = Text(screen=screen, text=args.get("text_error"))
    else:
        text_error = Text(screen=screen, text="")
    text_error.set_pos((400, 125))
    global all_buttons
    all_buttons = []

    def host():
        return 0

    def join():
        text_error.set_text("Подключение...")
        screen.fill(BG_COLOR)
        for button in all_buttons:
            button.img()
            button.draw()
        text_error.draw()
        text.draw()
        input.update()
        pygame.display.flip()
        try:
            PORT = int(input.text)
        except ValueError:
            PORT = 0
        return (2, {"PORT": PORT})

    all_buttons.append(
        Button(
            button_def=host,
            img_off=back_off_img,
            img_on=back_on_img,
            position=(225, 225),
            screen=screen,
        )
    )
    all_buttons.append(
        Button(
            button_def=join,
            img_off=go_off_img,
            img_on=go_on_img,
            position=(575, 225),
            screen=screen,
        )
    )

    text = Text(screen=screen, text="port: ")
    text.set_pos((75, 350))
    text_error.set_pos((400, 75))
    input = Input(
        count=4,
        only_nums=True,
        letter_size=40,
        screen=screen,
        FPS=def_fps,
        color=color,
        pos=(text.rect.right, text.rect.centery),
    )

    while y == None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in all_buttons:
                    if button.is_focus:
                        return button.click()
        screen.fill(BG_COLOR)
        for button in all_buttons:
            button.img()
            button.draw()
        text_error.draw()
        text.draw()
        input.update()
        pygame.display.flip()
        clock.tick(FPS)
    return y


def get_block_img(block_scale, color=color):
    r, g, b = color
    color4 = [r, g, b]
    color3 = [r - 21, g - 21, b - 21]
    color2 = [r - 42, g - 42, b - 42]
    color1 = [r - 63, g - 63, b - 63]
    colors = [color1, color2, color3, color4]
    for color in colors:
        for i in range(len(color)):
            if color[i] < 0:
                color[i] = 0
            elif color[i] > 255:
                color[i] = 255

    def get_img(map):
        img = pygame.Surface((len(map[0]), len(map)), pygame.SRCALPHA)
        img.fill((BG_COLOR[0], BG_COLOR[1], BG_COLOR[2], 0))
        for y in range(len(map)):
            for x in range(len(map[0])):
                color_id = map[y][x]
                if color_id != 0:
                    pixel = pygame.Surface((1, 1))
                    pixel.fill(colors[color_id - 1])
                    img.blit(pixel, (x, y))
        return img

    block_map = [
        [2, 3, 3, 3, 3, 3, 3, 4, 4, 4],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 4],
        [2, 0, 2, 2, 3, 3, 3, 3, 0, 4],
        [1, 0, 2, 0, 0, 0, 0, 3, 0, 3],
        [1, 0, 2, 0, 0, 0, 0, 3, 0, 3],
        [1, 0, 2, 0, 0, 0, 0, 3, 0, 3],
        [1, 0, 1, 0, 0, 0, 0, 2, 0, 3],
        [1, 0, 1, 1, 2, 2, 2, 2, 0, 3],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [1, 1, 1, 1, 1, 1, 1, 2, 2, 2],
    ]

    ball_map = [
        [0, 0, 0, 3, 3, 4, 4, 0, 0, 0],
        [0, 0, 3, 0, 0, 0, 0, 4, 0, 0],
        [0, 2, 0, 0, 3, 4, 0, 0, 4, 0],
        [2, 0, 0, 2, 0, 0, 4, 0, 0, 4],
        [2, 0, 2, 0, 0, 0, 0, 4, 0, 4],
        [2, 0, 2, 0, 0, 0, 0, 3, 0, 3],
        [2, 0, 0, 2, 0, 0, 2, 0, 0, 3],
        [0, 2, 0, 0, 2, 2, 0, 0, 3, 0],
        [0, 0, 2, 0, 0, 0, 0, 2, 0, 0],
        [0, 0, 0, 2, 2, 2, 2, 0, 0, 0],
    ]
    host_off_map = [
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 2, 0, 0, 0, 2, 2, 0, 0, 0, 2, 0, 0, 0, 0, 2],
        [2, 0, 0, 2, 0, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 2],
        [2, 0, 0, 2, 0, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 2],
        [2, 0, 0, 2, 0, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2],
        [2, 0, 0, 2, 2, 2, 2, 0, 2, 0, 0, 2, 0, 0, 2, 2, 0, 0, 0, 2, 0, 0, 0, 0, 2],
        [2, 0, 0, 2, 0, 0, 2, 0, 2, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 2],
        [2, 0, 0, 2, 0, 0, 2, 0, 2, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 2],
        [2, 0, 0, 2, 0, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 2],
        [2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0, 2, 2, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    ]
    host_on_map = [
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
        [3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3],
        [3, 2, 0, 3, 0, 0, 3, 0, 0, 3, 3, 0, 0, 0, 3, 3, 0, 0, 0, 3, 0, 0, 0, 2, 3],
        [3, 2, 0, 3, 0, 0, 3, 0, 3, 0, 0, 3, 0, 3, 0, 0, 3, 0, 0, 3, 0, 0, 0, 2, 3],
        [3, 2, 0, 3, 0, 0, 3, 0, 3, 0, 0, 3, 0, 3, 0, 0, 0, 0, 3, 3, 3, 3, 0, 2, 3],
        [3, 2, 0, 3, 0, 0, 3, 0, 3, 0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 2, 3],
        [3, 2, 0, 3, 3, 3, 3, 0, 3, 0, 0, 3, 0, 0, 3, 3, 0, 0, 0, 3, 0, 0, 0, 2, 3],
        [3, 2, 0, 3, 0, 0, 3, 0, 3, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 2, 3],
        [3, 2, 0, 3, 0, 0, 3, 0, 3, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 2, 3],
        [3, 2, 0, 3, 0, 0, 3, 0, 3, 0, 0, 3, 0, 3, 0, 0, 3, 0, 0, 3, 0, 0, 0, 2, 3],
        [3, 2, 0, 3, 0, 0, 3, 0, 0, 3, 3, 0, 0, 0, 3, 3, 0, 0, 0, 0, 3, 3, 0, 2, 3],
        [3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3],
        [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    ]
    join_off_map = [
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 2, 2, 0, 0, 2, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 2, 0, 0, 2, 2, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2],
        [2, 0, 0, 0, 2, 0, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 2, 2, 0, 0, 0, 2, 2, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    ]
    join_on_map = [
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
        [3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3],
        [3, 2, 0, 0, 0, 0, 0, 3, 0, 0, 3, 3, 0, 0, 3, 0, 3, 0, 0, 0, 3, 0, 0, 2, 3],
        [3, 2, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 2, 3],
        [3, 2, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 3, 0, 0, 2, 3],
        [3, 2, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 3, 0, 3, 0, 3, 3, 0, 0, 3, 0, 0, 2, 3],
        [3, 2, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 0, 2, 3],
        [3, 2, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 3, 0, 3, 0, 3, 0, 0, 3, 3, 0, 0, 2, 3],
        [3, 2, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 3, 0, 0, 2, 3],
        [3, 2, 0, 0, 3, 0, 0, 3, 0, 3, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 3, 0, 0, 2, 3],
        [3, 2, 0, 0, 0, 3, 3, 0, 0, 0, 3, 3, 0, 0, 3, 0, 3, 0, 0, 0, 3, 0, 0, 2, 3],
        [3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3],
        [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    ]
    back_off_map = [
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 4, 4, 4, 4, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 2, 0, 2, 3, 3, 3, 3, 4, 4, 4, 0, 0, 2],
        [2, 0, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 4, 4, 0, 0, 2],
        [2, 0, 0, 0, 1, 1, 0, 0, 2, 2, 0, 0, 0, 0, 3, 4, 0, 0, 2],
        [2, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 0, 0, 3, 3, 0, 0, 2],
        [2, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 0, 0, 3, 3, 0, 0, 2],
        [2, 0, 0, 0, 1, 1, 0, 0, 1, 2, 0, 0, 0, 0, 3, 3, 0, 0, 2],
        [2, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 2, 3, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 2, 2, 2, 2, 2, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    ]
    back_on_map = [
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
        [3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3],
        [3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3],
        [3, 2, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 4, 4, 4, 4, 0, 2, 3],
        [3, 2, 0, 0, 0, 0, 2, 0, 2, 3, 3, 3, 3, 4, 4, 4, 0, 2, 3],
        [3, 2, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 4, 4, 0, 2, 3],
        [3, 2, 0, 0, 1, 1, 0, 0, 2, 2, 0, 0, 0, 0, 3, 4, 0, 2, 3],
        [3, 2, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 0, 0, 3, 3, 0, 2, 3],
        [3, 2, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 0, 0, 3, 3, 0, 2, 3],
        [3, 2, 0, 0, 1, 1, 0, 0, 1, 2, 0, 0, 0, 0, 3, 3, 0, 2, 3],
        [3, 2, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 2, 3, 0, 2, 3],
        [3, 2, 0, 0, 0, 0, 1, 0, 1, 1, 1, 2, 2, 2, 2, 2, 0, 2, 3],
        [3, 2, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 0, 2, 3],
        [3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3],
        [3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3],
        [3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3],
        [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    ]
    go_off_map = [
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2],
        [2, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 2, 0, 0, 2],
        [2, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 2],
        [2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2],
        [2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2],
        [2, 0, 0, 2, 0, 0, 0, 2, 2, 2, 2, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2],
        [2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2],
        [2, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 2, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    ]
    go_on_map = [
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
        [3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3],
        [3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 2, 3],
        [3, 2, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 3, 0, 2, 3],
        [3, 2, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 3, 0, 2, 3],
        [3, 2, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 3, 0, 2, 3],
        [3, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 3, 0, 2, 3],
        [3, 2, 0, 3, 0, 0, 0, 3, 3, 3, 3, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 3, 0, 2, 3],
        [3, 2, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 3, 0, 2, 3],
        [3, 2, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 2, 3],
        [3, 2, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 3, 0, 2, 3],
        [3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3],
        [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    ]
    set_off_map = [
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 3, 3, 4, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 3, 3, 0, 3, 0, 4, 0, 4, 4, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 2, 0, 0, 3, 3, 0, 3, 4, 0, 0, 4, 0, 0, 0, 2],
        [2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 2, 0, 0, 3, 3, 3, 0, 0, 4, 0, 0, 0, 0, 2],
        [2, 0, 0, 2, 2, 2, 0, 1, 3, 0, 3, 3, 0, 3, 4, 4, 0, 0, 2],
        [2, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 2],
        [2, 0, 0, 1, 1, 1, 0, 1, 1, 0, 3, 3, 0, 3, 3, 3, 0, 0, 2],
        [2, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 3, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 2],
        [2, 0, 0, 0, 1, 0, 0, 1, 1, 0, 2, 2, 0, 0, 3, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 1, 1, 0, 1, 0, 2, 0, 2, 2, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    ]
    set_on_map = [
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
        [3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3],
        [3, 2, 0, 0, 0, 0, 0, 0, 3, 3, 4, 0, 0, 0, 0, 0, 0, 2, 3],
        [3, 2, 0, 0, 0, 3, 3, 0, 3, 0, 4, 0, 4, 4, 0, 0, 0, 2, 3],
        [3, 2, 0, 0, 2, 0, 0, 3, 3, 0, 3, 4, 0, 0, 4, 0, 0, 2, 3],
        [3, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 2, 3],
        [3, 2, 0, 0, 0, 2, 0, 0, 3, 3, 3, 0, 0, 4, 0, 0, 0, 2, 3],
        [3, 2, 0, 2, 2, 2, 0, 1, 3, 0, 3, 3, 0, 3, 4, 4, 0, 2, 3],
        [3, 2, 0, 1, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 3, 0, 2, 3],
        [3, 2, 0, 1, 1, 1, 0, 1, 1, 0, 3, 3, 0, 3, 3, 3, 0, 2, 3],
        [3, 2, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 3, 0, 0, 0, 2, 3],
        [3, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 2, 3],
        [3, 2, 0, 0, 1, 0, 0, 1, 1, 0, 2, 2, 0, 0, 3, 0, 0, 2, 3],
        [3, 2, 0, 0, 0, 1, 1, 0, 1, 0, 2, 0, 2, 2, 0, 0, 0, 2, 3],
        [3, 2, 0, 0, 0, 0, 0, 0, 1, 1, 2, 0, 0, 0, 0, 0, 0, 2, 3],
        [3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3],
        [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    ]
    imgs = [
        get_img(block_map),
        get_img(ball_map),
        get_img(host_off_map),
        get_img(host_on_map),
        get_img(join_off_map),
        get_img(join_on_map),
        get_img(back_off_map),
        get_img(back_on_map),
        get_img(go_off_map),
        get_img(go_on_map),
        get_img(set_off_map),
        get_img(set_on_map),
    ]
    imgs[0] = pygame.transform.scale(imgs[0], (block_scale, block_scale))
    imgs[1] = pygame.transform.scale(imgs[1], (block_scale, block_scale))
    imgs[2] = pygame.transform.scale(imgs[2], (scale_x_off, scale_y_off))
    imgs[3] = pygame.transform.scale(imgs[3], (scale_x_on, scale_y_on))
    imgs[4] = pygame.transform.scale(imgs[4], (scale_x_off, scale_y_off))
    imgs[5] = pygame.transform.scale(imgs[5], (scale_x_on, scale_y_on))
    imgs[6] = pygame.transform.scale(imgs[6], (scale_y_off, scale_y_off))
    imgs[7] = pygame.transform.scale(imgs[7], (scale_y_on, scale_y_on))
    imgs[8] = pygame.transform.scale(imgs[8], (scale_x_off, scale_y_off))
    imgs[9] = pygame.transform.scale(imgs[9], (scale_x_on, scale_y_on))
    imgs[10] = pygame.transform.scale(imgs[10], (50, 50))
    imgs[11] = pygame.transform.scale(imgs[11], (60, 60))
    return imgs


imgs = get_block_img(block_scale)
host_off_img = imgs[2]
host_on_img = imgs[3]
join_off_img = imgs[4]
join_on_img = imgs[5]
back_off_img = imgs[6]
back_on_img = imgs[7]
go_off_img = imgs[8]
go_on_img = imgs[9]
set_off_img = imgs[10]
set_on_img = imgs[11]


def game(
    args: dict = {
        "block_scale": 40,
        "SCREEN_WIDTH": 30,
        "SCREEN_HEIGHT": 20,
        "server": None,
        "is_host": False,
        "address": None,
    },
    pos_p1=None,
    other_player=None,
    block_scale: int = block_scale,
    SCREEN_WIDTH: int = 30,
    SCREEN_HEIGHT: int = 20,
    server: socket.socket = None,
    y=None,
    is_host: bool = False,
    address=None,
    FPS=120,
):
    block_scale = args.get("block_scale")
    block_img, ball_img = get_block_img(block_scale)[:2]
    time_ask_current = 0
    time_answer_current = 0
    time_ask = 3
    time_answer = 0.2
    SCREEN_WIDTH = args.get("SCREEN_WIDTH")
    SCREEN_HEIGHT = args.get("SCREEN_HEIGHT")
    server = args.get("server")
    address = args.get("address")
    is_host = args.get("is_host")
    p2_color = args.get("p2_color")
    nicks = [args.get("nick1"), args.get("nick2")]
    print(nicks)
    bg_2_color = text_to_other(args.get("p2_bg"))
    p2_img = get_block_img(block_scale, p2_color)[0]
    global score_p1
    score_p1 = [0]
    global score_p2
    score_p2 = [0]
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.Surface((SCREEN_WIDTH * block_scale, SCREEN_HEIGHT * block_scale))
    pygame.display.set_caption("ping_pong")
    pygame.mouse.set_visible(True)

    text_nick_p1 = Text(screen, nicks[0])
    text_nick_p2 = Text(screen, nicks[1], color=p2_color)

    text_score_p1 = Text(screen)
    text_score_p2 = Text(screen, color=p2_color)

    sep_score = Text(screen, ":")

    status_bar = pygame.Surface((20, 60))

    def set_pos_status_bar(status_bar=status_bar):
        if (
            str(score_p1[0]) != text_score_p1.text
            or str(score_p2[0]) != text_score_p2.text
        ):
            text_score_p1.set_text(str(score_p1[0]))
            text_score_p2.set_text(str(score_p2[0]))
            max_width = max(
                text_nick_p1.rect.width + text_score_p1.rect.width,
                text_nick_p2.rect.width + text_score_p2.rect.width,
            )
            width_bar = max_width * 2 + text_nick_p1.size * 2 + sep_score.rect.width

            text_nick_p1.rect.x = 0
            text_score_p1.rect.x = (
                max_width + text_nick_p1.size - text_score_p1.rect.width
            )
            sep_score.rect.x = int(max_width + text_nick_p1.size)
            text_score_p2.rect.x = width_bar - max_width - text_nick_p1.size
            text_nick_p2.rect.x = width_bar - text_nick_p2.rect.width

            text_nick_p1.rect.y = text_nick_p2.rect.y = text_score_p1.rect.y = (
                text_score_p2.rect.y
            ) = sep_score.rect.y = 10
            status_bar = pygame.Surface((width_bar, 60))
        status_bar.fill(BG_COLOR)
        for i in [text_nick_p1, text_nick_p2, text_score_p1, text_score_p2, sep_score]:
            i.screen = status_bar
            i.draw()
        all_screen.blit(
            status_bar,
            (int((all_screen.get_rect().width - status_bar.get_rect().width) / 2), 0),
        )
        return status_bar

    class Block:
        def __init__(
            self,
            image,
            position_left_top,
            speed: int = 0,
            min=0,
            max=SCREEN_HEIGHT * block_scale,
        ):
            self.is_pressed = True
            self.min = min
            self.max = max
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.inflate_ip(0, 0)
            self.rect.left, self.rect.top = position_left_top
            self.speed = speed * block_scale / 8 * def_fps / FPS
            self.angle = 0
            self.is_cheat_ball = False

        def draw(self):
            rotated_image = pygame.transform.rotate(self.image, self.angle)
            rotated_rect = rotated_image.get_rect(center=self.rect.center)
            screen.blit(rotated_image, rotated_rect)

        def update(self):
            if CHEATS:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_c]:
                    if not (self.is_pressed):
                        self.is_pressed = True
                        self.is_cheat_ball = not (self.is_cheat_ball)
                else:
                    self.is_pressed = False
            if not (self.is_cheat_ball) or not (CHEATS):
                if self.speed != 0:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_w]:
                        self.rect.y -= self.speed
                    if key[pygame.K_s]:
                        self.rect.y += self.speed
                    if CHEATS:
                        if key[pygame.K_d]:
                            self.rect.x += self.speed
                        if key[pygame.K_a]:
                            self.rect.x -= self.speed
                    self.border()
            self.draw()

        def border(self):
            if self.rect.top < self.min:
                self.rect.top = self.min
            if self.rect.bottom > self.max:
                self.rect.bottom = self.max

    class Ball:
        def __init__(
            self, image, speed, position_center=screen.get_rect().center, goal_def=null, max: int = 3
        ):
            self.goal = goal_def
            self.max = max
            self.count_of_speed = 0
            self.image: pygame.Surface = image
            self.angle = 0
            self.speed = speed * block_scale / 8 * def_fps / FPS
            self.speed2 = speed * block_scale / 8 * def_fps / FPS
            self.position = position_center
            self.rect: pygame.Rect = self.image.get_rect()
            self.rect.inflate_ip(0, 0)
            self.rect.x, self.rect.y = self.position
            self.vector = randint(1, 4)
            self.is_visible = True
            self.current_image = image
            self.is_cheat_pos = False
            self.is_pressed = False

        def set_visible(self, is_visible: bool):
            if self.is_visible != is_visible:
                self.is_visible = is_visible
                if not (is_visible):
                    self.rect.center = screen.get_rect().center
                    self.speed2 = self.speed
                    self.speed = 0
                    self.count_of_speed = 0

        def new_rect_speed(self):
            speed_now = int(self.speed + self.count_of_speed / self.max)
            for i in range(speed_now):
                self.new_rect: pygame.Rect = self.rect
                self.old_rect: pygame.Rect = self.rect
                if self.vector < 3:
                    self.new_rect.y -= 1
                else:
                    self.new_rect.y += 1
                if self.vector in [2, 3]:
                    self.new_rect.x += 1
                else:
                    self.new_rect.x -= 1
                self.rect = self.new_rect
                self.border()

        def border(self):
            block_orig = self
            for block in blocks:
                if self.rect.colliderect(block.rect):
                    if (
                        abs(block.rect.x - self.rect.x)
                        + abs(block.rect.y - self.rect.y)
                        < abs(block_orig.rect.x - self.rect.x)
                        + abs(block_orig.rect.y - self.rect.y)
                        or block_orig == self
                    ):
                        block_orig = block

            if block_orig != self:
                if abs(self.old_rect.y - block_orig.rect.y) > abs(
                    self.rect.x - block_orig.rect.x
                ):
                    if self.rect.y < block_orig.rect.y:
                        if self.vector == 4:
                            self.vector = 1
                        elif self.vector == 3:
                            self.vector = 2
                    else:
                        if self.vector == 1:
                            self.vector = 4
                        elif self.vector == 2:
                            self.vector = 3
                elif abs(self.rect.y - block_orig.rect.y) < abs(
                    self.rect.x - block_orig.rect.x
                ):
                    if self.old_rect.x < block_orig.rect.x:
                        if self.vector == 2:
                            self.vector = 1
                        elif self.vector == 3:
                            self.vector = 4
                    else:
                        if self.vector == 1:
                            self.vector = 2
                        elif self.vector == 4:
                            self.vector = 3
                else:
                    self.vector = 5 - self.vector
                if block_orig.speed != 0:
                    self.count_of_speed += 1
                self.rect = self.old_rect
                self.new_rect_speed()

        def cheat_rect(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.new_rect.y -= self.speed
            elif keys[pygame.K_s]:
                self.new_rect.y += self.speed
            if keys[pygame.K_a]:
                self.new_rect.x -= self.speed
            elif keys[pygame.K_d]:
                self.new_rect.x += self.speed

        def update(self):
            if CHEATS:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_c]:
                    if not (self.is_pressed):
                        self.is_pressed = True
                        self.is_cheat_pos = not (self.is_cheat_pos)
                else:
                    self.is_pressed = False
            if self.is_cheat_pos:
                self.cheat_rect()
            else:
                self.new_rect_speed()
            if self.rect.left < 0:
                if is_host:
                    self.goal(False)
            elif self.rect.right > screen.get_width():
                if is_host:
                    self.goal(True)
            self.draw()

        def draw(self):
            rotated_image = pygame.transform.rotate(self.current_image, self.angle)
            rotated_rect = rotated_image.get_rect(center=self.rect.center)
            screen.blit(rotated_image, rotated_rect)

    global blocks
    blocks = []

    global balls
    balls = []

    def spawn_player(len: int = 3, speed=1, is_local=True, img=block_img):
        blocks_count = len
        player = []
        for i in range(blocks_count):
            if is_local:
                block = Block(
                    image=block_img,
                    position_left_top=(
                        0,
                        i * block_scale
                        + (
                            int(SCREEN_HEIGHT * block_scale / 2)
                            - int(blocks_count * block_scale / 2)
                        ),
                    ),
                    speed=speed,
                    min=(i + 1) * block_scale,
                    max=SCREEN_HEIGHT * block_scale - (blocks_count - i) * block_scale,
                )
            else:
                block = Block(
                    image=img,
                    position_left_top=(
                        (SCREEN_WIDTH - 1) * block_scale,
                        i * block_scale
                        + (
                            int(SCREEN_HEIGHT * block_scale / 2)
                            - int(blocks_count * block_scale / 2)
                        ),
                    ),
                    speed=0,
                    min=(i + 1) * block_scale,
                    max=SCREEN_HEIGHT * block_scale - (blocks_count - i) * block_scale,
                )
            blocks.append(block)
            player.append(block)
        return player

    def spawn_map():
        for i in range(SCREEN_WIDTH):
            if i < int(SCREEN_WIDTH / 2):
                block = Block(
                    image=block_img,
                    position_left_top=(i * block_scale, 0),
                )
                blocks.append(block)
                block = Block(
                    image=block_img,
                    position_left_top=(
                        i * block_scale,
                        (SCREEN_HEIGHT - 1) * block_scale,
                    ),
                )
                blocks.append(block)
            else:
                block = Block(
                    image=p2_img,
                    position_left_top=(i * block_scale, 0),
                )
                blocks.append(block)
                block = Block(
                    image=p2_img,
                    position_left_top=(
                        i * block_scale,
                        (SCREEN_HEIGHT - 1) * block_scale,
                    ),
                )
                blocks.append(block)

    def new_round():
        balls[0].speed = balls[0].speed2
        balls[0].vector = randint(1, 4)
        balls[0].set_visible(True)

    def spawn_ball(
        speed: int = 1,
    ):
        balls.append(Ball(ball_img, speed, goal_def=None))
        new_round()

    bg_2 = pygame.Surface((SCREEN_WIDTH * block_scale, SCREEN_HEIGHT * block_scale))
    bg_2.fill(bg_2_color)
    time_ask = int(FPS * time_ask)
    time_answer = int(FPS * time_answer)
    start_speed_ball = 1
    start_speed_player = 2
    player = spawn_player(
        get_p_len(SCREEN_HEIGHT),
        speed=start_speed_player / 8 * (SCREEN_HEIGHT - 2),
    )
    other_player = spawn_player(
        get_p_len(SCREEN_HEIGHT),
        speed=start_speed_player / 8 * (SCREEN_HEIGHT - 2),
        is_local=False,
        img=p2_img,
    )
    spawn_map()
    spawn_ball(start_speed_ball * (SCREEN_WIDTH - 2) / 14)

    global timer
    timer = [0, null]

    def wait(time: int | float, func):
        timer[0] = time * FPS
        timer[1] = func

    def goal(is_me):
        if is_me:
            score_p1[0] += 1
        else:
            score_p2[0] += 1
        balls[0].set_visible(False)
        wait(3, new_round)

    balls[0].goal = goal

    is_answered = False
    all_screen = pygame.display.set_mode((screen.get_width(), screen.get_height() + 60))
    status_bar = set_pos_status_bar()
    while y == None:
        if is_host:
            if timer[0] >= 0:
                timer[0] -= 1
            if timer[0] < 0:
                timer[0] = 0
                timer[1]()
                timer[1] = null
            datas = {
                "pos_p1": [player[0].rect.x, player[0].rect.y],
                "pos_ball": [balls[0].rect.x, balls[0].rect.y],
                "vector_ball": balls[0].vector,
                "speed_ball": balls[0].speed,
                "vis_ball": balls[0].is_visible,
                "is_cheat": balls[0].is_cheat_pos,
                "p2": score_p1[0],
                "p1": score_p2[0],
            }
            send(
                server=server,
                text=encode(datas),
                address=address,
            )
            if time_ask_current == 0:
                is_answered = False

            time_ask_current += 1
            if time_ask_current >= time_ask:
                time_ask_current = 0
            if not (is_answered):
                time_answer_current += 1
            data = ""
            try:
                while True:
                    data, _ = server.recvfrom(1024)
            except BlockingIOError:
                data = decode(data)
                if type(data) is dict:
                    if str(data.get("message")) == version:
                        time_answer_current = 0
                        is_answered = True
                        pos_p2 = data.get("pos_p2")
                        for i in range(len(other_player)):
                            block: Block = other_player[i]
                            block.rect.x, block.rect.y = [
                                (SCREEN_WIDTH - 1) * block_scale - pos_p2[0],
                                pos_p2[1] + i * block_scale,
                            ]
            except ConnectionResetError:
                server.close()
                return (0, {"text_error": "клиент покинул игру!"})
            finally:
                if time_answer_current >= time_answer:
                    server.close()
                    return (0, {"text_error": "клиент не отвечает"})
        else:
            data = ""
            try:
                send(
                    server=server,
                    text=encode(
                        {
                            "message": version,
                            "pos_p2": [player[0].rect.x, player[0].rect.y],
                        }
                    ),
                    address=address,
                )
                while True:
                    data, _ = server.recvfrom(1024)
            except BlockingIOError:
                if data != "":
                    data: dict = decode(data)
                    ball: Ball = balls[0]
                    ball.rect.x, ball.rect.y = [
                        (SCREEN_WIDTH - 1) * block_scale - data.get("pos_ball")[0],
                        data.get("pos_ball")[1],
                    ]
                    vector = data.get("vector_ball")
                    if vector == 1:
                        vector = 2
                    elif vector == 2:
                        vector = 1
                    elif vector == 3:
                        vector = 4
                    else:
                        vector = 3
                    ball.vector = vector
                    ball.speed = data.get("speed_ball")
                    pos_p1 = data.get("pos_p1")
                    ball.set_visible(data.get("vis_ball"))
                    ball.is_cheat_pos = data.get("is_cheat")
                    score_p1[0] = data.get("p1")
                    score_p2[0] = data.get("p2")
                    for i in range(len(other_player)):
                        block: Block = other_player[i]
                        block.rect.x, block.rect.y = [
                            (SCREEN_WIDTH - 1) * block_scale - pos_p1[0],
                            pos_p1[1] + i * block_scale,
                        ]
            except ConnectionResetError:
                server.close()
                return (0, {"text_error": "потеряно соединение с сервером!"})

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                server.close()
                y = (0, {"text_error": "вы покинули игру"})

        screen.fill(BG_COLOR)
        screen.blit(bg_2, (int(SCREEN_WIDTH * block_scale / 2), 0))

        for block in blocks:
            block.update()
        for ball in balls:
            ball.update()

        all_screen.fill(BG_COLOR)
        all_screen.blit(screen, (0, 60))
        set_pos_status_bar(status_bar)
        pygame.display.flip()
        clock.tick(FPS)

    return y


def start_menu(args: dict = {"text_error": ""}, y=None, FPS=30):
    text_error = args.get("text_error")
    pygame.init()
    screen_w = 800
    screen_h = 400
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("MainMenu")
    pygame.mouse.set_visible(True)
    if text_error != "":
        text = Text(screen=screen, text=text_error)
        text.set_pos((int(screen_w / 2), int(screen_h / 2) - 125))
    else:
        text = Text(screen=screen, text=f"version {version}")
        text.set_pos((int(screen_w / 2), int(screen_h / 2) - 125))
    pygame.display.set_caption("Menu")
    pygame.mouse.set_visible(True)

    global all_buttons
    all_buttons = []

    def host():
        return 1

    def join():
        return 5

    def settings():
        return 6

    all_buttons.append(
        Button(
            button_def=host,
            img_off=host_off_img,
            img_on=host_on_img,
            position=(225, 225),
            screen=screen,
        )
    )
    all_buttons.append(
        Button(
            button_def=join,
            img_off=join_off_img,
            img_on=join_on_img,
            position=(575, 225),
            screen=screen,
        )
    )
    all_buttons.append(Button(settings, set_off_img, set_on_img, (750, 50), screen))

    while y == None:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 4
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in all_buttons:
                        if button.is_focus:
                            return button.click()

            screen.fill(BG_COLOR)
            for button in all_buttons:
                button.img()
                button.draw()
            if text != None:
                text.draw()

            pygame.display.flip()
            clock.tick(FPS)
        except KeyboardInterrupt:
            y = 4

    return y


def send(server: socket.socket, text, address):
    if type(text) is str:
        text = encode(text)
    server.sendto(text, address)


def encode(massage):
    if type(massage) is dict:
        items = massage.items()
        massage = []
        for key, value in items:
            massage.append(key + "=" + str(value))
        massage = " , ".join(massage)
    return str(massage).encode("utf-8")


def decode(massage: bytes):
    if type(massage) is not bytes:
        return massage
    massage = massage.decode("utf-8")
    try:
        massage = massage.split(" , ")
        try:
            d = dict()
            for i in massage:
                item = i.split("=")
                d[item[0]] = text_to_other(item[1])
            massage = d
        except:
            pass
    except:
        pass
    return massage


def host_menu(PORT=None, y=None):
    nickname = all_settings.get("nickname")
    pygame.init()
    PORT = randint(1000, 9999)
    HOST = "0.0.0.0"
    BUFFER_SIZE = 1024

    # Создание UDP-сокета
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Привязка к адресу и порту
    server.bind((HOST, PORT))
    server.setblocking(False)

    screen_w = 800
    screen_h = 400
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("HostMenu")

    global all_buttons
    all_buttons = []

    def host():
        server.close()
        return 0

    all_buttons.append(
        Button(
            button_def=host,
            img_off=back_off_img,
            img_on=back_on_img,
            position=(400, 225),
            screen=screen,
        )
    )

    text = Text(text=f"port {PORT}!", screen=screen)
    text.set_pos((int(screen_w / 2), int(screen_h / 2) - 125))

    text_p2 = Text(text="ожидание 2-о игрока...", screen=screen)
    text_p2.set_pos((int(screen_w / 2), int(screen_h / 2 - 100)))

    while y == None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in all_buttons:
                    if button.is_focus:
                        return button.click()
        text.draw()
        text_p2.draw()
        try:
            data, addr = server.recvfrom(BUFFER_SIZE)
            data = decode(data)
            nick_p2 = data.get("nick")
            p2_color = text_to_other(data.get("p2_color"))
            p2_bg = text_to_other(data.get("p2_bg"))
            text_p2 = Text(screen=screen, text=f"p2: {nick_p2}")
            text_p2.set_pos((int(screen_w / 2), int(screen_h / 2 - 100)))
            # Можно сразу отправить ответ обратно
            server.sendto(
                encode(
                    f"block_scale={block_scale} , SCREEN_WIDTH={SCREEN_WIDTH} , SCREEN_HEIGHT={SCREEN_HEIGHT} , COLOR={color} , BG={BG_COLOR} , nick_other={nickname}"
                ),
                addr,
            )
            return (
                3,
                {
                    "block_scale": block_scale,
                    "SCREEN_WIDTH": SCREEN_WIDTH,
                    "SCREEN_HEIGHT": SCREEN_HEIGHT,
                    "server": server,
                    "is_host": True,
                    "address": addr,
                    "player_len": get_p_len(SCREEN_HEIGHT),
                    "p2_color": p2_color,
                    "p2_bg": p2_bg,
                    "nick1": nickname,
                    "nick2": nick_p2,
                },
            )
        except BlockingIOError:
            pass
        except KeyboardInterrupt:
            error = "Сервер остановлен"
            return (0, {"text_error": error})
        screen.fill(BG_COLOR)
        text.draw()
        for button in all_buttons:
            button.img()
            button.draw()

        pygame.display.flip()
        clock.tick(def_fps)

    server.close()
    return 0


def join_menu(args: dict):
    PORT = args.get("PORT")
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.setblocking(False)
    BUFFER_SIZE = 1024
    SERVER_ADDR = ("255.255.255.255", PORT)
    server.sendto(
        encode(
            {"nick": all_settings.get("nickname"), "p2_color": color, "p2_bg": BG_COLOR}
        ),
        SERVER_ADDR,
    )
    time_wait = 2
    time_frame = 0.1
    max_k = int(time_wait / time_frame)
    k = 0
    while True:
        try:
            data, SERVER_ADDR = server.recvfrom(BUFFER_SIZE)
            data = decode(data)
            params = []
            for key in data.keys():
                params.append(text_to_other(data.get(key)))
            block_scale_host, SCREEN_WIDTH, SCREEN_HEIGHT, p2_color, p2_bg, nick_p2 = (
                params
            )
            return (
                3,
                {
                    "block_scale": block_scale_host,
                    "SCREEN_WIDTH": SCREEN_WIDTH,
                    "SCREEN_HEIGHT": SCREEN_HEIGHT,
                    "server": server,
                    "is_host": False,
                    "address": SERVER_ADDR,
                    "p2_color": p2_color,
                    "p2_bg": p2_bg,
                    "nick1": all_settings.get("nickname"),
                    "nick2": nick_p2,
                },
            )
        except BlockingIOError:
            k += 1
            if k > max_k:
                error = "Ошибка сервера!"
                return (5, {"text_error": error})
        except OSError:
            error = "Ошибка сервера!"
            return (5, {"text_error": error})
        except ConnectionResetError:
            error = "Потеряно соединение с сервером!"
            return (5, {"text_error": error})
        time.sleep(time_frame)


def bye(time=end_time):
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1000, 600))
    screen.fill(BG_COLOR)
    text = "Закрытие..."
    text = Text(screen, text, 100)
    text.set_pos((int(screen.get_width() / 2), int(screen.get_height() / 2)))
    for _ in range(time):
        text.draw()
        pygame.display.flip()
        clock.tick(1)
    pygame.quit()
    # os.remove('data.txt')
    return "exit"


def main_settings():
    pygame.init()
    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption("Settings")
    pygame.mouse.set_visible(True)
    text = Text(screen, "Введите никнейм:")
    text.set_pos((400, 100))
    nick_input = Input(
        15,
        False,
        60,
        screen,
        def_fps,
        all_settings.get("nickname"),
        pos=(int(screen.get_width() / 2), int(screen.get_height() / 2)),
    )

    all_buttons = []

    def back():
        return (0, {"text_error": "Настройки сохранены"})

    back_off_img2 = pygame.transform.scale(back_off_img, (50, 50))
    back_on_img2 = pygame.transform.scale(back_on_img, (60, 60))
    all_buttons.append(Button(back, back_off_img2, back_on_img2, (50, 50), screen))

    def save():
        try:
            with open("data.txt", "r") as file:
                old_settings = to_dict(file.read())
                print(old_settings)
                if nick_input.text != "":
                    old_settings["nickname"] = nick_input.text
                    all_settings["nickname"] = nick_input.text
                print(old_settings)
                file.close()
            with open("data.txt", "w") as file:
                file.write(str(old_settings))
                file.close()
        except:
            return (0, {"text_error": "Ошибка при сохранении настроек!"})

    y = None
    while y == None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in all_buttons:
                    if button.is_focus:
                        return button.click()
        screen.fill(BG_COLOR)
        text.draw()
        nick_input.update()
        for button in all_buttons:
            button.img()
            button.draw()
        nick_input.text_obj.rect.center = (
            int(screen.get_width() / 2),
            int(screen.get_height() / 2),
        )
        all_settings["nickname"] = nick_input.text
        clock.tick(def_fps)
        pygame.display.flip()
    save()
    return y


def main():
    defs = [start_menu, host_menu, join_menu, game, bye, join_input_menu, main_settings]
    n = defs[0]()
    while True:
        try:
            if type(n) is int:
                n = defs[n]()
            elif type(n) is tuple:
                if len(n) == 1:
                    n = defs[n[0]]()
                else:
                    n = defs[n[0]](args=n[1])
            elif type(n) is str:
                break
        except:
            n = defs[0](args={"text_error": "Неизвестная ошибка!"})


main()
