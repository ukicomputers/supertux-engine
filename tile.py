# TODO: fix magic 3
from config import SNOW_TILES, TILE_SHADOWS, TILE_CUTS
import pygame as pg

class Tiles:
    def __init__(self):
        tileTypes = [SNOW_TILES]
        self.tiles = {}
        self.blockType: str = "snow"

        for tileType in tileTypes:
            for key, value in tileType.items():
                self.tiles[key] = pg.image.load(value).convert_alpha()

    def getHeight(self, height: int, includeTop: bool = True):
        result = self.tiles[self.blockType + "Block"].get_size()[1] * height
        if includeTop:
            result += self.tiles[self.blockType + "Top"].get_size()[1]
        return result

    # returns hitbox
    def drawTiles(self, screen: pg.Surface, position: tuple[int, int], height: int, width: int):
        block = self.tiles[self.blockType + "Block"]
        blockTop = self.tiles[self.blockType + "Top"]
        blockW, blockH = block.get_size()
        blockTopW, blockTopH = blockTop.get_size()

        centerWidth = blockW - 2 * TILE_SHADOWS
        left = block.subsurface((0, 0, TILE_SHADOWS, blockH))
        center = block.subsurface((TILE_SHADOWS, 0, centerWidth, blockH))
        right = block.subsurface((TILE_SHADOWS + centerWidth, 0, TILE_SHADOWS, blockH))

        topBlockWidth = blockTopW - 2 * TILE_CUTS
        leftBlockPart = blockTop.subsurface((0, 0, TILE_CUTS, blockTopH))
        centerBlockPart = blockTop.subsurface((TILE_CUTS, 0, topBlockWidth, blockTopH))
        rightBlockPart = blockTop.subsurface((TILE_CUTS + topBlockWidth, 0, TILE_CUTS, blockTopH))

        # draw top part
        screen.blit(leftBlockPart, position)

        for w in range(width):
            topX = position[0] + TILE_CUTS + w * topBlockWidth
            part = centerBlockPart
            
            if w % 2 != 0:
                part = pg.transform.flip(part, True, False)
            
            screen.blit(part, (topX, position[1]))

        # draw bottom part
        rightX = position[0] + TILE_CUTS + width * topBlockWidth
        screen.blit(rightBlockPart, (rightX, position[1]))

        for h in range(height):
            baseY = position[1] + h * blockH + blockTopH - 3

            for w in range(width):
                baseX = position[0] + w * centerWidth + 3
                screen.blit(center, (baseX + TILE_SHADOWS, baseY))

                if w == 0:
                    screen.blit(left, (baseX, baseY))

                if w == width - 1:
                    screen.blit(right, (baseX + TILE_SHADOWS + centerWidth, baseY))

        # return hitboxes
        return {
            "type": "tile",
            "rects": {
                "top": pg.Rect(position[0] + TILE_CUTS, position[1], topBlockWidth * width, blockTopH // 2),
                "left": pg.Rect(position[0] + 10, position[1] + blockTopH - 3, 1, blockH * height),
                "right": pg.Rect(position[0] + 3 + 2 * TILE_SHADOWS + centerWidth * width - 10, position[1] + blockTopH - 3, 1, blockH * height),
                "bottom": pg.Rect(position[0] + 10, position[1] + blockTopH + blockH * height - 3, centerWidth * width + TILE_SHADOWS, 1)
            }
        }