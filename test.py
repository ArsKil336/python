import pygame

pygame.init()

def get_colored_png(path: str, color: tuple):
    image = pygame.image.load(path).convert_alpha()
    colored_image = pygame.Surface(image.get_size()).convert_alpha()
    colored_image.fill(color)
    image.blit(colored_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)


get_colored_png("set_on.png", (255, 0, 0))
