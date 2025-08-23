from config import ENEMY_FADE_DURATION, SPRITE_FPS, MOVE_STEPS, ENEMY_DIE_DELAY
from sounds import Sounds
import pygame as pg

class Enemy:
    def __init__(self, sprites, position: tuple[int, int], xFix: int, soundController: Sounds):
        self.sprite = sprites["snowball"]
        self.rect: pg.Rect = self.sprite["walkImgs"][0].get_rect()
        self.initialX = position[0]
        self.xFix = xFix
        self.rect.bottomright = position

        self.currentAnimation = 0
        self.lastAnimationTime = None
        self.dead = False

        self.sounds = soundController

        self.alpha = 255
        self.deadTime = None

    def finished(self):
        return self.dead

    def kill(self):
        if self.dead:
            return
        self.sounds.snowballDie()
        self.dead = True
        self.deadTime = pg.time.get_ticks()

    def increaseAnimation(self):
        now = pg.time.get_ticks()

        if not self.lastAnimationTime:
            self.lastAnimationTime = now
            return

        if now - self.lastAnimationTime < SPRITE_FPS:
            return

        if not self.dead:
            if self.rect.right < self.xFix:
                self.rect.right += MOVE_STEPS
                if self.rect.right > self.xFix:
                    self.rect.right = self.xFix
                    self.initialX, self.xFix = self.xFix, self.initialX
            else:
                self.rect.right -= MOVE_STEPS
                if self.rect.right < self.xFix:
                    self.rect.right = self.xFix
                    self.initialX, self.xFix = self.xFix, self.initialX

        self.currentAnimation += 1
        if self.currentAnimation >= len(self.sprite["walkImgs"]):
            self.currentAnimation = 0

        if self.dead and self.deadTime is not None:
            elapsed = now - self.deadTime
            if elapsed >= ENEMY_DIE_DELAY:
                fadeElapsed = elapsed - ENEMY_DIE_DELAY
                if fadeElapsed >= ENEMY_FADE_DURATION:
                    self.alpha = 0
                else:
                    t = fadeElapsed / ENEMY_FADE_DURATION
                    self.alpha = int(255 * (1.0 - t))

        self.lastAnimationTime = now

    def draw(self, screen: pg.Surface):
        self.increaseAnimation()
        output = {
            "type": "enemy",
            "rects": {
                "body": pg.Rect(self.rect.left, self.rect.top + int(self.rect.height * 0.2), self.rect.width, self.rect.height),
                "top": pg.Rect(self.rect.left + 10, self.rect.top, self.rect.width - 10, int(self.rect.height * 0.2))
            },
            "kill": self.kill,
            "finished": self.finished
        }

        if self.finished():
            return output

        if self.dead:
            coin = self.sprite["squished"].copy()
            coin.set_alpha(max(0, min(255, self.alpha)))
            oldBottom = self.rect.bottom
            self.rect.width, self.rect.height = coin.get_size()
            self.rect.bottom = oldBottom
        else:
            coin = self.sprite["walkImgs"][self.currentAnimation]

        if self.rect.right < self.xFix:
            coin = pg.transform.flip(coin, True, False)

        screen.blit(coin, self.rect)

        return output