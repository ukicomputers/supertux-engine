from config import LEVEL_DIRECTIORY
from os.path import join
from sounds import Sounds
from images import Background
from tile import Tiles
from tux import Tux
from coin import Coin
from score import Score
from block import Block
from enemy import Enemy
import pygame as pg
import json

def loadLevel(
        levelName: str, 
        screen: pg.Surface, 
        tileController: Tiles, 
        soundController: Sounds, 
        bkg: Background, 
        tux: Tux,
        score: Score,
        sprites,
        objectSprites
    ):
    screenH = screen.get_height()

    with open(join(LEVEL_DIRECTIORY, levelName + ".json"), "r") as f:
        levelData = json.load(f)

    bkg.setBackground(levelData["background"])
    soundController.setBgMusic(levelData["bgMusic"])
    soundController.startBgMusic()
    tileController.blockType = levelData["theme"]
    tux.rect.left = levelData["startPosition"][0]
    tux.rect.bottom = levelData["startPosition"][1]

    # load general objects
    coins: list[Coin] = []
    blocks: list[Block] = []
    enemies: list[Enemy] = []

    for part in levelData["elements"]:
        position = (part["startPosition"][0], part["startPosition"][1])

        if part["type"] == "coin":
            coins.append(Coin(objectSprites, position, score, soundController))
        elif part["type"] == "block":
            maxCoins = part.get("maxCoins", 1)
            blocks.append(Block(objectSprites, position, soundController, score, part["subtype"], maxCoins))
        elif part["type"] == "enemy":
            enemies.append(Enemy(sprites, position, part["fix"], soundController))

    # render method
    def render():
        bkg.draw(screen)
        collisionBoxes = []

        for part in levelData["elements"]:
            # TODO: just make each Tile class for each tile
            if part["type"] == "tile":
                x = part["startPosition"][0]
                y = part["startPosition"][1]

                if y == "bottom":
                    y = screenH - tileController.getHeight(part["height"])
                collisionBoxes.append(tileController.drawTiles(screen, (x, y), part["height"], part["width"]))

        for coin in coins:
            if not coin.finished():
                collisionBoxes.append(coin.draw(screen))
            else:
                coins.remove(coin)

        for block in blocks:
            collisionBoxes.append(block.draw(screen))

        for enemy in enemies[:]:
            if enemy.alpha > 0:
                collisionBoxes.append(enemy.draw(screen))
            else:
                enemies.remove(enemy)
        
        return collisionBoxes

    return render