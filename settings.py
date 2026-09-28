import pygame as pg

WIDTH = 1024
HEIGHT = 768
TITLE =  "w game"
TILESIZE = 32
FPS = 30

# colors
WHITE = (255, 255, 255)
GREEN = (144, 238, 144)
DARK_GREEN = (46, 96, 33)
RED = (255, 0, 0)
PURPLE = (82, 14, 125)
TAN = (210, 180, 140)
BLACK = (0, 0, 0)


# player settings
PLAYER_SPEED = 300
PLAYER_HIT_RECT = pg.Rect(0,0, TILESIZE - 5, TILESIZE - 5)