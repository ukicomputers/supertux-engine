from config import SCORE_FONT, FONT_SIZE, FONT_COLOR, FONT_PADDING, COINS, FONT_IMAGE_PADDING
import pygame as pg

class Score:
    def __init__(self, screenW: int):
        pg.font.init()
        self.font = pg.font.Font(SCORE_FONT, FONT_SIZE)
        self.screenW = screenW
        self.coinsImage = pg.image.load(COINS).convert_alpha()
        self.coins: int = 0 # TODO: maybe add coins of coins
        self.currentView: pg.Surface = None
        self._renderFont()

    def _renderFont(self):
        self.currentView = self.font.render(str(self.coins), True, FONT_COLOR)

    def addCoins(self, coins = 1):
        self.coins += coins
        self._renderFont()
    
    def draw(self, screen: pg.Surface):
        textRect = self.currentView.get_rect()
        textRect.top = FONT_PADDING
        textRect.right = self.screenW - FONT_PADDING
        
        coinsRect = self.coinsImage.get_rect()
        coinsRect.right = textRect.left - FONT_IMAGE_PADDING
        coinsRect.centery = textRect.centery

        screen.blit(self.currentView, textRect)
        screen.blit(self.coinsImage, coinsRect)