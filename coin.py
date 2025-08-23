from config import COIN_FPS, MOVE_STEPS
from sounds import Sounds
from score import Score
import pygame as pg

class Coin:
    def __init__(self, sprites, position: tuple[int, int], score: Score, soundController: Sounds):
        self.sprite = sprites["coin"]
        self.rect: pg.Rect = self.sprite["idle"].get_rect()
        self.currentAnimation = 0
        self.lastAnimationTime = None
        self.score = score
        self.rect.bottomright = position
        self.collected = False
        self.alpha = 255
        self.alphaSteps = self.alpha // (2 * self.rect.height // MOVE_STEPS)
        self.sounds = soundController

    def finished(self):
        return self.alpha == 0

    def collect(self):
        if self.collected:
            return
        
        self.score.addCoins()
        self.sounds.coinSound()
        self.collected = True

    def draw(self, screen: pg.Surface):
        if self.finished():
            return

        now = pg.time.get_ticks()

        if not self.lastAnimationTime:
            self.lastAnimationTime = now

        if self.collected:
            self.rect.bottom -= MOVE_STEPS
            if self.rect.bottom > 2 * self.rect.height:
                self.alpha = max(0, self.alpha - self.alphaSteps)

        coin = self.sprite["animations"][self.currentAnimation].copy()
        coin.set_alpha(self.alpha)
        screen.blit(coin, self.rect)

        if now - self.lastAnimationTime >= COIN_FPS:
            self.currentAnimation += 1
            if self.currentAnimation >= len(self.sprite["animations"]):
                self.currentAnimation = 0
            self.lastAnimationTime = now

        return { "type": "coin", "rect": self.rect, "collect": self.collect }