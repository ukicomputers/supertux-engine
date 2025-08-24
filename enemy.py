from config import ENEMY_FADE_DURATION, SPRITE_FPS, MOVE_STEPS, ENEMY_DIE_DELAY
from sounds import Sounds
import pygame as pg

class Enemy:
    def __init__(self, sprites, position: tuple[int, int], maximalX: int, soundController: Sounds):
        self.sprite = sprites["snowball"]
        self.rect: pg.Rect = self.sprite["walkImgs"][0].get_rect()
        self.minimalX = position[0]
        self.maximalX = maximalX
        self.rect.bottomright = position

        self.currentAnimation = 0
        self.lastAnimationTime = None
        self.dead = False

        self.sounds = soundController

        self.alpha = 255
        self.deadTime = None

    def finished(self):
        return self.alpha == 0

    def kill(self):
        if self.dead:
            return
        
        self.sounds.snowballDie()
        self.dead = True
        coin = self.sprite["squished"]
        oldBottom = self.rect.bottom
        self.rect.width, self.rect.height = coin.get_size()
        self.rect.bottom = oldBottom
        self.deadTime = pg.time.get_ticks()

    def _increaseAnimation(self):
        now = pg.time.get_ticks()

        if not self.lastAnimationTime:
            self.lastAnimationTime = now
            return

        if now - self.lastAnimationTime < SPRITE_FPS:
            return
        
        if self.rect.right < self.maximalX:
            self.rect.right += MOVE_STEPS
            if self.rect.right > self.maximalX:
                self.rect.right = self.maximalX
                self.minimalX, self.maximalX = self.maximalX, self.minimalX
        else:
            self.rect.right -= MOVE_STEPS
            if self.rect.right < self.maximalX:
                self.rect.right = self.maximalX
                self.minimalX, self.maximalX = self.maximalX, self.minimalX

        self.currentAnimation += 1
        if self.currentAnimation >= len(self.sprite["walkImgs"]):
            self.currentAnimation = 0

        self.lastAnimationTime = now

    def draw(self, screen: pg.Surface):
        output = {
            "type": "enemy",
            "rects": {
                "body": pg.Rect(self.rect.left, self.rect.top + int(self.rect.height * 0.2), self.rect.width, self.rect.height - int(self.rect.height * 0.2)),
                "top": pg.Rect(self.rect.left, self.rect.top, self.rect.width, int(self.rect.height * 0.2))
            },
            "kill": self.kill,
            "finished": self.dead
        }

        if self.dead:
            coin = self.sprite["squished"].copy()

            now = pg.time.get_ticks()
            elapsed = now - self.deadTime
            
            if elapsed >= ENEMY_DIE_DELAY:
                fadeElapsed = elapsed - ENEMY_DIE_DELAY
                if fadeElapsed >= ENEMY_FADE_DURATION:
                    self.alpha = 0
                else:
                    self.alpha = int(255 * (1.0 - fadeElapsed / ENEMY_FADE_DURATION))
                
                coin.set_alpha(self.alpha)
        else:
            self._increaseAnimation()
            coin = self.sprite["walkImgs"][self.currentAnimation]

        if self.rect.right < self.maximalX:
            coin = pg.transform.flip(coin, True, False)

        screen.blit(coin, self.rect)
        return output