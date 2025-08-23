from config import BACKGROUNDS
import pygame as pg

def loadSprites(sprites):
    sprites = sprites.copy()

    for value in sprites.values():  
        for key, path in value.items():
            if isinstance(path, str):
                value[key] = pg.image.load(path).convert_alpha()
            elif isinstance(path, list):
                value[key] = [pg.image.load(img).convert_alpha() for img in sorted(path)]

    return sprites

class Background:
    def __init__(self, screenSize: tuple[int, int]):
        self.bkgs = {}
        self.screenSize = screenSize

        for bkg, value in BACKGROUNDS.items():
            self.bkgs[bkg] = pg.transform.smoothscale(pg.image.load(value["path"]).convert_alpha(), screenSize)

        self.topGradient: pg.Surface = None
        self.background: str = None
    
    def setBackground(self, background):
        self.background = background
        self.topGradient = None

        if "upperGradient" in BACKGROUNDS[background]:
            gradient = BACKGROUNDS[background]["upperGradient"]
            self.topGradient = pg.Surface((1, len(gradient)))
            for i in range(len(gradient)):
                self.topGradient.set_at((0, i), BACKGROUNDS[background]["upperGradient"][i])
            self.topGradient = pg.transform.smoothscale(self.topGradient, self.screenSize)
    
    def draw(self, screen: pg.Surface):
        if not self.background:
            return
        
        screen.fill("black")

        if self.topGradient:
            screen.blit(self.topGradient, (0, 0))
        
        screen.blit(self.bkgs[self.background], (0, 0))

class Shade:
    def __init__(self, size: tuple[int, int]):
        self.overlay = pg.Surface(size)
        self.overlay.fill((0, 0, 0))
        self.distance = size[1] // 2
    
    def draw(self, screen: pg.Surface, playerY: int):
        remaining = max(0, screen.get_height() - playerY)
        frac = 1.0 - remaining / self.distance
        alpha = int(max(0, min(255, 255 * frac)))
        self.overlay.set_alpha(alpha)
        screen.blit(self.overlay.convert_alpha(), (0, 0))