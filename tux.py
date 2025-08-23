from config import SPRITE_FPS
from sounds import Sounds
import pygame as pg

class Tux:
    def __init__(self, sprites, soundController: Sounds, currentForm: str = "smallTux"):
        self.sprites = {
            "smallTux": sprites["small_tux"],
            "bigTux": sprites["big_tux"]
        }

        self.form = currentForm

        self.lastAnimationTime = None
        self.rect = pg.Rect(0, 0, 0, 0)
        self.forwardDirection = True
        self.currentAnimation = {"type": "idle"}
        self.sound = soundController

        self._initRect()

    def _initRect(self):
        self.rect.width, self.rect.height = self._getSprite().get_size()
        
    def _increaseAnimation(self):
        imgs = None

        if self.currentAnimation["type"] == "walk":
            imgs = "walkImgs"
        elif self.currentAnimation["type"] == "kill":
            imgs = "killImgs"
        else:
            return
        
        now = pg.time.get_ticks()

        if not self.lastAnimationTime:
            self.lastAnimationTime = now
            return

        if now - self.lastAnimationTime < SPRITE_FPS:
            return
            
        sprite = self.sprites[self.form]

        self.currentAnimation["id"] += 1
        if self.currentAnimation["id"] >= len(sprite[imgs]):
            self.currentAnimation["id"] = 0

        self._initRect()
        self.lastAnimationTime = now
    
    def _getSprite(self) -> pg.Surface:
        if self.currentAnimation["type"] == "walk":
            return self.sprites[self.form]["walkImgs"][self.currentAnimation["id"]]
        elif self.currentAnimation["type"] == "kill":
            return self.sprites[self.form]["killImgs"][self.currentAnimation["id"]]
        else:
            return self.sprites[self.form][self.currentAnimation["type"]]

    def draw(self, screen: pg.Surface):
        sprite = self._getSprite()

        if not self.forwardDirection:
            sprite = pg.transform.flip(sprite, True, False)

        screen.blit(sprite, self.rect.topleft)
        self._increaseAnimation()

    def jump(self):
        if self.currentAnimation["type"] == "jump":
            return
        
        self.currentAnimation = {"type": "jump"}
    
    def setDirection(self, goRight=True):
        self.forwardDirection = goRight

    def walk(self):
        if self.currentAnimation["type"] == "walk":
            return

        self.currentAnimation = {"type": "walk", "id": 0}

    def kill(self):
        if self.currentAnimation["type"] == "kill":
            return
        
        self.sound.dieSound()

        if self.form != "smallTux":
            self.form = "smallTux"
        
        self.currentAnimation = {"type": "kill", "id": 0}
    
    def changeForm(self, form: str):
        if self.form == "smallTux" and form != "smallTux":
            self.sound.yahooSound()
        self.form = form

    def down(self):
        if self.form == "smallTux":
            return
        
        self.currentAnimation = {"type": "down"}
    
    def idle(self):
        if self.lastAnimationTime:
            diff = pg.time.get_ticks() - self.lastAnimationTime
            if diff < SPRITE_FPS:
                return

        self.lastAnimationTime = None
        self.currentAnimation = {"type": "idle"}