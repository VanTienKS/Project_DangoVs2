import pygame
from os import walk


def import_image(path):
    images = pygame.image.load(path).convert_alpha()
    return images


def import_folder(path):
    surface_list = []
    for _, __, img_files in walk(path):
        for image in img_files:
            surface_list.append(import_image(path + '/' + image))
    return surface_list

def import_foulder_dict(path):
    surface_dict = {}
    for _, __, img_files in walk(path):
        for image in img_files:
            surface_dict[image.split('.')[0]] = import_image(path + '/' + image)
    return surface_dict


def debug(surface, content, pos, color):
    font = pygame.font.Font(None, 30)

    font_surface = font.render(str(content), True, color)
    font_rect = font_surface.get_rect(center=pos)

    surface.blit(font_surface, font_rect)

