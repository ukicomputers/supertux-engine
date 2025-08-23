from sounds import Sounds
from coin import Coin
from score import Score
from config import EXPLOSION_BLOCK, HINT_BLOCK, ANGLE_ADDITION, BLOCK_ACTIVATION_DELAY
import pygame as pg

# types:
# - wood
# - woodCoin
# - blue
# - bluePowerup
# - purple
class Block:
    def __init__(self, sprites, position: tuple[int, int], soundController: Sounds, score: Score, type: str = "wood", coins: int = 1):
        self.sprites = {
            "purple": sprites["purpleBonus"],
            "blue": sprites["blueBonus"],
            "wood": sprites["snowWoodBrick"],
            "coin": sprites["coin"]
        }

        self.sound = soundController
        self.form = type
        self.currentAnimation = 0
        self.lastAnimationTime = None
        self.finished = False
        self.coin: list[Coin] = []
        self.rect = pg.Rect(0, 0, 0, 0)
        self.rect.bottomright = position
        self.score = score
        self.leftCoins = coins

        self.lastHitTime = None
        
        self.angle = 0
        self.angleAddition = 0

    def _increaseAnimation(self):
        now = pg.time.get_ticks()

        if not self.lastAnimationTime:
            self.lastAnimationTime = now
            return
        
        delay = HINT_BLOCK
        if self.form == "wood" and self.finished:
            delay = EXPLOSION_BLOCK

        if now - self.lastAnimationTime < delay:
            return
            
        self.currentAnimation += 1
        if self.currentAnimation >= len(self.sprites[self.form]["animations"]):
            self.currentAnimation = 0

        self.lastAnimationTime = now

    def _getCurrentSprite(self) -> pg.Surface:
        sprite = None

        if self.form == "wood" or self.form == "woodCoin":
            if not self.finished:
                sprite = self.sprites["wood"]["empty"]
            else:
                sprite = self.sprites["wood"]["animations"][self.currentAnimation]
        elif self.form == "blue":
            if not self.finished:
                sprite = self.sprites["blue"]["animations"][self.currentAnimation]
            else:
                sprite = self.sprites["blue"]["empty"]
        elif self.form == "purple":
            if not self.finished:
                sprite = self.sprites["purple"]["animations"][self.currentAnimation]
            else:
                sprite = self.sprites["purple"]["empty"]
        
        size = sprite.get_size()
        self.rect.width = size[0]
        self.rect.height = size[1]
        return sprite

    def hit(self, centerX):
        if self.finished:
            return
        
        now = pg.time.get_ticks()
        if self.lastHitTime:
            if now - self.lastHitTime < BLOCK_ACTIVATION_DELAY:
                return
        
        self.sound.brickSound()
        self._getCurrentSprite()

        if centerX < self.rect.centerx:
            self.angleAddition = -ANGLE_ADDITION
        elif centerX > self.rect.centerx:
            self.angleAddition = ANGLE_ADDITION

        if self.form == "blue" or self.form == "woodCoin" or self.form == "purple":
            if self.leftCoins - 1 >= 0:
                self.leftCoins -= 1
                self.coin.append(Coin(self.sprites, self.rect.bottomright, self.score, self.sound))
                self.coin[-1].collect()
                if self.leftCoins == 0:
                    self.finished = True

        self.lastHitTime = now

    def draw(self, screen: pg.Surface):
        for coin in self.coin:
            coin.draw(screen)
            if coin.finished():
                self.coin.remove(coin)

        if self.angleAddition != 0:
            self.angle += self.angleAddition
            
            if self.angle <= -15:
                self.angle = -15
                self.angleAddition = ANGLE_ADDITION
            elif self.angle >= 15:
                self.angleAddition = -ANGLE_ADDITION
                self.angle = 15
            elif self.angle == 0:
                self.angleAddition = 0
            
        rotatedSprite = pg.transform.rotate(self._getCurrentSprite(), self.angle)
        self.rect.width = rotatedSprite.get_width()
        self.rect.height = rotatedSprite.get_height()

        screen.blit(rotatedSprite, self.rect.topleft)
        
        self._increaseAnimation()

        return {
            "type": "block",
            "rects": {
                "top": pg.Rect(self.rect.left + 10, self.rect.top, self.rect.width - 10, 1),
                "left": pg.Rect(self.rect.left, self.rect.top + 10, 1, self.rect.height - 10),
                "right": pg.Rect(self.rect.right, self.rect.top + 10, 1, self.rect.height - 10),
                "bottom": pg.Rect(self.rect.left + 10, self.rect.bottom, self.rect.width - 10, 1)
            },
            "hit": self.hit
        }