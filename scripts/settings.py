from pygame.math import Vector2
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 800
FPS = 60

TILE_SIZE = 64
FONT_SIZE = 30

COLOR_TEXT = (255,255,255)


# overlay positions
OVERLAY_POSITIONS = {
    'tool':(40, SCREEN_HEIGHT - 15),
    'seed':(100, SCREEN_HEIGHT - 15),
}

PLAYER_TOOL_OFFSET = {
	'left': Vector2(-50,25),
	'right': Vector2(50,25),
	'up': Vector2(10,-25),
	'down': Vector2(-10,50)
}

LAYERS = {
    'water': 0,
    'ground': 1,
    'soil': 2,
    'soil water': 3,
    'rain floor': 4,
    'house bottom': 5,
    'ground plant': 6,
    'main': 7,
    'house top': 8,
    'fruit': 9,
    'rain drops': 10,
}

APPLE_POS = {
	'Small': [(18,17), (30,37), (12,50), (30,45), (20,30), (30,10)],
	'Large': [(30,24), (60,65), (50,50), (16,40),(45,50), (42,70)]
}

GROW_SPEED = {
    'corn': 1,
    'tomato': 0.7,
}

SALE_PRICES = {
    'wood': 4,
    'apple': 2,
    'corn': 10,
    'tomato': 20,
}

PURCHASE_PRICES = {
    'corn': 5,
    'tomato': 8,
}
