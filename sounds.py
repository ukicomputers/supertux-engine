from config import (
    SOUNDS, 
    SOUND_FADE_TIME, 
    BG_MUSIC_LEVEL, 
    FG_MUSIC_LEVEL
)

import pygame as pg

class Sounds:
    def __init__(self):
        pg.mixer.init()
        self.mixerMusic = {}
        self.bgMusic = "first"

        for category, value in SOUNDS.items():
            self.mixerMusic[category] = {}
            for musicName, musicPath in value.items():
                self.mixerMusic[category][musicName] = pg.mixer.Sound(musicPath)
                if category == "effects":
                    self.mixerMusic[category][musicName].set_volume(FG_MUSIC_LEVEL)
                else:
                    self.mixerMusic[category][musicName].set_volume(BG_MUSIC_LEVEL)
    
    def jumpSound(self):
        self.mixerMusic["effects"]["jump"].play()

    def dieSound(self):
        self.mixerMusic["effects"]["kill"].play()
    
    def setBgMusic(self, music: str):
        self.bgMusic = music
    
    def startBgMusic(self):
        self.mixerMusic["music"][self.bgMusic].play(loops=-1, fade_ms=SOUND_FADE_TIME)

    def unpauseBgMusic(self):
        self.mixerMusic["music"][self.bgMusic].unpause()

    def pauseBgMusic(self):
        self.mixerMusic["music"][self.bgMusic].pause()

    def coinSound(self):
        self.mixerMusic["effects"]["coin"].play()

    def yahooSound(self):
        self.mixerMusic["effects"]["yahoo"].play()

    def brickSound(self):
        self.mixerMusic["effects"]["brick"].play()
    
    def snowballDie(self):
        self.mixerMusic["effects"]["snowball"].play()