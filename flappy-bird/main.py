#!/usr/bin/env python
# -*- coding: utf-8 -*-
import taichi as ti

ti.init(arch=ti.gpu)

SCREEN_WIDTH = 288
SCREEN_HEIGH = 512

PIPE_WIDTH = 50
PIPE_HEIGH = 300
PIPE_GAP_SIZE = 100

BIRD_WIDTH = 20
BIRD_HEIGH = 20

FLOOR_HEIGH = 80
BASE_HEIGH = SCREEN_HEIGH - FLOOR_HEIGH

FPS = 60
GRAVITY_CONSTANT = 9.8

class Rect():
    def __init__(self, pos, width, heigh):
        self.left = pos[0] - width / 2
        self.right = pos[0] + width / 2
        self.top = pos[1] - heigh / 2
        self.bottom = pos[1] + heigh / 2
        print(self.left)
        print(self.right)
        print(self.top)
        print(self.bottom)

    def updatePos(self, speed, pos_type):
        if pos_type == 0:
            self.top -= speed
            self.bottom -= speed
        else:
            self.top += speed
            self.bottom += speed

    def getTop(self):
        return self.top
    
    def setTop(self, val):
        self.top = val
    
    def getBottom(self):
        return self.bottom
    
    def setBottom(self, val):
        self.bottom = val

    def getTopLeft(self):
        return [self.left, self.top]
    
    def getBottomRight(self):
        return [self.right, self.bottom]

class Bird():
    def __init__(self, pos):
        self.is_flapped = False
        self.is_touch_boudary = False
        self.up_speed = 10
        self.down_speed = 0
        self.time_pass = FPS / 1000000
        self.rect = Rect(pos, BIRD_WIDTH / SCREEN_WIDTH, BIRD_HEIGH / SCREEN_HEIGH)

        
    def update(self):
        if self.is_flapped:
            self.up_speed -= GRAVITY_CONSTANT * self.time_pass
            self.rect.updatePos(self.up_speed, 0)
            if self.up_speed <= 0:
                self.down()
                self.up_speed = 10
                self.down_speed = 0
        else:
            self.down_speed += GRAVITY_CONSTANT / 2 * self.time_pass
            self.rect.updatePos(self.down_speed, 1)

        if self.rect.getTop() <= 0:
            self.up_speed = 0
            self.is_dead = True
            self.rect.setTop(0)

        if self.rect.getBottom() >= BASE_HEIGH:
            self.up_speed = 0
            self.is_dead = True
            self.down_speed = 0
            self.rect.setBottom(BASE_HEIGH)
        
        print("p1 = ", self.rect.left, self.rect.top)
        print("p2 = ", self.rect.right, self.rect.bottom)

    def up(self):
        if self.is_flapped:
            self.up_speed = max(12, self.up_speed + 1)
        else:
            self.is_flapped = True

    def down(self):
        self.is_flapped = False


    def draw(self, gui):
        # gui.rect(self.rect.getTopLeft(), self.rect.getBottomRight(), color=0xff0000)
        gui.rect([0.2, 0.2], [0.3, 0.3], color=0x00ff00)
        gui.rect([0.2, 0.4], [0.3, 0.5], color=0xff0000)
        gui.rect([0.1, 0.2], [0.2, 0.3], color=0x0000bb)


class Pipe():
    def __init__(self, pos):
        print("a")

    def gen():
        print("a")

    def draw(self, gui):
        print("a")


class Monitor():
    gui = ti.GUI("flappy bird", (SCREEN_WIDTH, SCREEN_HEIGH))

    def __init__(self):
        self.bird = Bird([0.3, 0.5])
        
    def drawScore(self):
        print("a")

    def drawGameOver(self):
        print("a")

    def draw(self):
        while Monitor.gui.running:
            for e in Monitor.gui.get_events(ti.GUI.PRESS):
                if e.key == ti.GUI.ESCAPE:
                    exit()
                elif e.key == ti.GUI.UP:
                    print("press up key")
                    # self.bird.up()
                elif e.key == ti.GUI.DOWN:
                    print("press down key")
                elif e.key == ti.GUI.LEFT:
                    print("press LEFT key")
                elif e.key == ti.GUI.RIGHT:
                    print("press right key")

            # self.bird.update()
            self.bird.draw(Monitor.gui)
            Monitor.gui.show()



monitor = Monitor()
monitor.draw()
