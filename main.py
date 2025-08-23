from config import (
    FPS, 
    MOVE_JUMP, 
    MOVE_LEFT, 
    MOVE_RIGHT,
    MOVE_SMALL,
    TUX_JUMP_HEIGHT, 
    GRAVITY, 
    EXIT_KEY,
    MOVE_STEPS,
    LEVEL_NAME,
    SPRITES,
    OBJECTS
)

import pygame as pg
from sounds import Sounds
import images
from tux import Tux
import physics
from tile import Tiles
from score import Score
from typing import Callable
import level

# general pygame
pg.init()
screen = pg.display.set_mode(flags=pg.FULLSCREEN)
screenW, screenH = screen.get_size()
clk = pg.time.Clock()

# sounds
soundController = Sounds()

# load player looks
sprites = images.loadSprites(SPRITES)
objects = images.loadSprites(OBJECTS)

# load backgrounds
bkg = images.Background((screenW, screenH))

# initialize player
player = Tux(sprites, soundController, "bigTux")

# calculate speeds
jumpSpeed = physics.jumpSpeed(TUX_JUMP_HEIGHT)
deadSpeed = physics.jumpSpeed(screenH // 2)

# score drawing
score = Score(screenW)

# load tiles
tiles = Tiles()

# dead shades
shade = images.Shade((screenW, screenH))

# load level
renderLevel = level.loadLevel(
    LEVEL_NAME, 
    screen, 
    tiles, 
    soundController, 
    bkg, 
    player,
    score,
    sprites,
    objects
)

# variables
spaceActive = False
jumping = False

gameEnded = False
endDirection = False

dy = 0
minY = screenH

running = True
while running:
    clk.tick(FPS)
    pg.event.pump()
    keys = pg.key.get_pressed()

    if keys[EXIT_KEY]:
        running = False
    
    if not gameEnded:
        lastRect = player.rect.copy()
        walking = False
        down = False

        if not keys[MOVE_SMALL]:
            if not keys[MOVE_LEFT] or not keys[MOVE_RIGHT]:
                if keys[MOVE_LEFT]:
                    walking = True
                    player.rect.left -= MOVE_STEPS
                    player.setDirection(False)
                elif keys[MOVE_RIGHT]:
                    walking = True
                    player.rect.left += MOVE_STEPS
                    player.setDirection()

            if keys[MOVE_JUMP] and not spaceActive and not jumping:
                spaceActive = True
                jumping = True
                soundController.jumpSound()
                dy = -jumpSpeed

            if not keys[MOVE_JUMP]:
                spaceActive = False
                if dy < 0:
                    dy *= 0.5
        else:
            down = True

        player.rect.bottom += dy
        dy += GRAVITY

        # draw level
        collision = renderLevel()

        if player.rect.left < 0:
            player.rect.left = 0
            walking = False
        elif player.rect.right > screenW:
            player.rect.right = screenW
            walking = False
        
        if player.rect.bottom > minY:
            player.rect.bottom = minY
            jumping = False
            dy = 0

            if player.rect.bottom >= screenH:
                gameEnded = True
                dy = -deadSpeed

        onTop = False
        def checkObjectCollision(
                rects: dict[str, pg.Rect],
                onTopCall: Callable[[], None] | None = None, 
                onLeftRightCall: Callable[[], None] | None = None, 
                onBottomCall: Callable[[], None] | None = None
            ):
            global onTop, walking, minY, jumping, dy
            for position, box in rects.items():
                if player.rect.colliderect(box):
                    if position == "left" or position == "right":
                        player.rect.left = lastRect.left
                        walking = False
                        if not onTop:
                            minY = screenH
                            jumping = True
                        
                        if onLeftRightCall:
                            onLeftRightCall()
                    elif position == "bottom":
                        dy = 1
                        minY = screenH

                        if onBottomCall:
                            onBottomCall()
                    else:
                        onTop = True
                        jumping = False
                        if not down and (keys[MOVE_LEFT] or keys[MOVE_RIGHT]):
                            walking = True
                        minY = box.bottom

                        if onTopCall:
                            onTopCall()
                elif not onTop:
                    minY = screenH
                    jumping = True
                    walking = False

        onTop = False
        for block in collision:
            if block["type"] == "tile":
                checkObjectCollision(block["rects"])
            elif block["type"] == "coin":
                if player.rect.colliderect(block["rect"]):
                    block["collect"]()
            elif block["type"] == "block":
                def hit():
                    block["hit"](player.rect.centerx)
                checkObjectCollision(block["rects"], onBottomCall=hit)
            elif block["type"] == "enemy":
                if not block["finished"]():
                    for position, box in block["rects"].items():
                        if player.rect.colliderect(box):
                            if position == "top":
                                block["kill"]()

                                if block["finished"]():
                                    dy = -jumpSpeed
                                    jumping = True
                            else:
                                if player.form == "smallTux":
                                    gameEnded = True
                                else:
                                    dy = -jumpSpeed
                                    player.changeForm("smallTux")
        
        if not gameEnded:
            if jumping:
                player.jump()
            elif walking:
                player.walk()
            elif down:
                player.down()
            else:
                player.idle()
    else:
        player.kill()
        renderLevel()

        if not endDirection:
            player.rect.bottom += dy
            dy += GRAVITY

            if player.rect.bottom <= screenH // 2:
                dy = 0
                endDirection = True
        else:
            player.rect.bottom += dy
            dy += GRAVITY

            if player.rect.top >= screenH:
                running = False

    player.draw(screen)
    score.draw(screen)

    if endDirection:
        shade.draw(screen, player.rect.bottom)

    pg.display.update()

pg.quit()