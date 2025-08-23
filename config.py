# utility
from os.path import join, isfile
from os import listdir
import pygame as pg

def getFiles(dir):
    files = []
    for f in listdir(dir):
        fPath = join(dir, f)
        if isfile(fPath):
            files.append(fPath)
    return files

# general
FPS = 60
ASSET_FOLDER = "assets"
MOVE_RIGHT = pg.K_RIGHT
MOVE_LEFT = pg.K_LEFT
MOVE_JUMP = pg.K_SPACE
MOVE_SMALL = pg.K_DOWN
EXIT_KEY = pg.K_ESCAPE

# level
LEVEL_NAME = "welcome"

# sounds
MUSIC_FOLDER = join(ASSET_FOLDER, "sounds")
EFFECTS_FOLDER = join(MUSIC_FOLDER, "effects")
BGMUSIC_FOLDER = join(MUSIC_FOLDER, "music")

SOUNDS = {
    "effects": {
        "jump": join(EFFECTS_FOLDER, "jump.wav"),
        "kill": join(EFFECTS_FOLDER, "kill.wav"),
        "coin": join(EFFECTS_FOLDER, "coin.wav"),
        "yahoo": join(EFFECTS_FOLDER, "grow.wav"),
        "brick": join(EFFECTS_FOLDER, "brick.wav"),
        "snowball": join(EFFECTS_FOLDER, "squish.wav")
    },
    "music": {
        "first": join(BGMUSIC_FOLDER, "first.ogg")
    }
}

SOUND_FADE_TIME = 2000 # ms
BG_MUSIC_LEVEL = 0.8
FG_MUSIC_LEVEL = 1.0

# sprites
SPRITE_FOLDER = join(ASSET_FOLDER, "sprites")
_small_tux_folder = join(SPRITE_FOLDER, "tux/small")
_big_tux_folder = join(SPRITE_FOLDER, "tux/big")

SPRITES = {
    "small_tux": {
        "walkImgs": getFiles(join(_small_tux_folder, "walk")),
        "killImgs": getFiles(join(_small_tux_folder, "kill")),
        "idle": join(_small_tux_folder, "walk/walk-5.png"),
        "jump": join(_small_tux_folder, "jump/jump.png")
    },
    "big_tux": {
        "walkImgs": getFiles(join(_big_tux_folder, "walk")),
        "idle": join(_big_tux_folder, "walk/walk-6.png"),
        "jump": join(_big_tux_folder, "jump/jump-0.png"),
        "down": join(_big_tux_folder, "down/duck-0.png")
    },
    "snowball": {
        "walkImgs": getFiles(join(SPRITE_FOLDER, "snowball")),
        "squished": join(SPRITE_FOLDER, "snowball/squished/squished-left.png")
    }
}

SPRITE_FPS = 100 # ms
COIN_FPS = 65
EXPLOSION_BLOCK = 150
HINT_BLOCK = 100
ANGLE_ADDITION = 2.5
BLOCK_ACTIVATION_DELAY = 500
ENEMY_DIE_DELAY = 2000
ENEMY_FADE_DURATION = 1000
TUX_JUMP_HEIGHT = 200 # px

# tiles
TILE_FOLDER = join(ASSET_FOLDER, "tiles")
TILE_SHADOWS = 16 # px from beginning and end
TILE_CUTS = 18.5

SNOW_TILES = {
    "snowBlock": join(TILE_FOLDER, "snow_block.png"),
    "snowTop": join(TILE_FOLDER, "snow_top.png")
}

# background
BACKGROUND_FOLDER = join(ASSET_FOLDER, "backgrounds")
BACKGROUNDS = {
    "arcticClouds": {
        "path": join(BACKGROUND_FOLDER, "arctis2.png"),
        "upperGradient": [(103, 154, 255), (168, 197, 255)]
    }
}

# objects
OBJECTS_FOLDER = join(ASSET_FOLDER, "objects")
OBJECTS = {
    "coin": {
        "animations": getFiles(join(OBJECTS_FOLDER, "coin")),
        "idle": join(OBJECTS_FOLDER, "coin/coin-0.png")
    },
    "blueBonus": {
        "animations": getFiles(join(OBJECTS_FOLDER, "blueBonus")),
        "empty": join(OBJECTS_FOLDER, "blueBonus/empty/empty.png")
    },
    "purpleBonus": {
        "animations": getFiles(join(OBJECTS_FOLDER, "purpleBonus")),
        "empty": join(OBJECTS_FOLDER, "purpleBonus/empty/purple_empty.png")
    },
    "snowWoodBrick": {
        "animations": getFiles(join(OBJECTS_FOLDER, "woodBrick/exploded")),
        "empty": join(OBJECTS_FOLDER, "woodBrick/snowbrick.png")
    }
}

# score
SCORE_FONT = join(ASSET_FOLDER, "fonts/stx.ttf")
COINS = join(ASSET_FOLDER, "fonts/coins.png")
FONT_SIZE = 20
FONT_COLOR = (255, 255, 153)
FONT_PADDING = 20
FONT_IMAGE_PADDING = 10

# physics
GRAVITY = 0.07 # to 1
MOVE_STEPS = 3

# level
LEVEL_DIRECTIORY = "levels"