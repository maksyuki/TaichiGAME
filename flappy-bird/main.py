#!/usr/bin/env python
# -*- coding: utf-8 -*-
import taichi as ti
import random
from PIL import Image
import numpy as np

ti.init(arch=ti.gpu)

SCREEN_WIDTH = 288
SCREEN_HEIGH = 512

PIPE_WIDTH = 50
PIPE_GAP_SIZE = 50

BIRD_WIDTH = 20
BIRD_HEIGH = 20

FLOOR_HEIGH = 80
BASE_HEIGH = SCREEN_HEIGH - FLOOR_HEIGH

FPS = 60
GRAVITY_CONSTANT = -9.8
DELTA_UP_VEC = 2
DELTA_UP_VEC_LIMIT = 4

class Bird():
    def __init__(self, pos):
        self.is_touch_boudary = False
        self.delta_time = FPS / 10000.0
        self.vec = 0
        self.pos = pos


    def update(self):
        if self.pos[1] + BIRD_HEIGH / 2 >= SCREEN_HEIGH or self.pos[1] - BIRD_HEIGH / 2 < FLOOR_HEIGH:
            self.is_touch_boudary = True
            self.vec = 0
        else:
            self.vec += GRAVITY_CONSTANT * self.delta_time

        self.pos[1] += self.vec


    def up(self):
        self.vec += max(DELTA_UP_VEC_LIMIT, DELTA_UP_VEC)

    def down(self):
        print("down")

    def calcX(self, sig):
        return (self.pos[0] + sig * BIRD_WIDTH / 2) / SCREEN_WIDTH
    
    def calcY(self, sig):
        return (self.pos[1] + sig * BIRD_HEIGH / 2) / SCREEN_HEIGH

    def draw(self, gui):
        gui.rect([self.calcX(-1), self.calcY(1)], [self.calcX(1), self.calcY(-1)], color=0xff0000)


class Pipe():
    def __init__(self, pos, heigh):
        self.pos = pos
        self.heigh = heigh
        self.vec = 10
        self.delta_time = FPS / 500.0

    def update(self):
        self.pos[0] -= self.vec * self.delta_time
        

    def calcX(self, sig):
        return (self.pos[0] + sig * PIPE_WIDTH) / SCREEN_WIDTH

    def calcY(self, low, sig):
        if low == 0:
            if sig == 0: return (FLOOR_HEIGH + self.heigh) / SCREEN_HEIGH
            else: return FLOOR_HEIGH / SCREEN_HEIGH
        else:
            if sig == 0: return SCREEN_HEIGH / SCREEN_HEIGH
            else: return (FLOOR_HEIGH + self.heigh + PIPE_GAP_SIZE) / SCREEN_HEIGH

    def draw(self, gui):
        gui.rect([self.calcX(0), self.calcY(0,0)], [self.calcX(1), self.calcY(0,1)], color=0xffffff)
        gui.rect([self.calcX(0), self.calcY(1,0)], [self.calcX(1), self.calcY(1,1)], color=0xffffff)


class Monitor():
    gui = ti.GUI("flappy bird", (SCREEN_WIDTH, SCREEN_HEIGH))

    def __init__(self):
        self.bird = Bird([0.3 * SCREEN_WIDTH, 0.5 * SCREEN_HEIGH])
        self.pipes = []
        self.pipes.append(Pipe([1 * SCREEN_WIDTH, FLOOR_HEIGH], self.genRandHeigh()))
        self.pipes.append(Pipe([1.5 * SCREEN_WIDTH, FLOOR_HEIGH], self.genRandHeigh()))
        self.bgd_img = np.array(Image.open('./resources/bgd-img-day.png').convert("RGB")).swapaxes(0, 1)
        self.bgd_img = np.flip(self.bgd_img, axis=1)
        self.game_over = np.array(Image.open('./resources/gameover.png').convert("RGB")).swapaxes(0, 1)
        self.game_over = np.flip(self.game_over, axis=1)
        print(self.game_over.ndim)
        print(self.game_over.shape)
        # print(self.game_over[0, 2])
        # print(self.game_over[0, 41])
        for i in range(192):
            for j in range(42):
                self.bgd_img[0+i, 256+j] = self.game_over[i, j]


    def movePipe(self):
        for p in self.pipes:
            if p.pos[0] >= 0 and p.pos[0] < 10:
                p.pos[0] = 1 * SCREEN_WIDTH
                p.heigh = self.genRandHeigh()

    def genRandHeigh(self):
        return random.randint(FLOOR_HEIGH + 40, FLOOR_HEIGH + 140)

    def drawScore(self):
        print("drawScore")

    def drawGameOver(self):
        print("drawGameOver")

    def drawGround(self):
        Monitor.gui.line([0, FLOOR_HEIGH / SCREEN_HEIGH], [1, FLOOR_HEIGH / SCREEN_HEIGH], color=0xffffff)

    def draw(self):
        # self.drawGameOver()
        while Monitor.gui.running:
            for e in Monitor.gui.get_events(ti.GUI.PRESS):
                if e.key == ti.GUI.ESCAPE:
                    exit()
                elif e.key == ti.GUI.UP:
                    print("press up key")
                    self.bird.up()
                elif e.key == ti.GUI.DOWN:
                    print("press down key")
                elif e.key == ti.GUI.LEFT:
                    print("press LEFT key")
                elif e.key == ti.GUI.RIGHT:
                    print("press right key")

            # for p in self.pipes:
                # p.update()
                # p.draw(Monitor.gui)

            # self.movePipe()
            # self.bird.update()
            # self.bird.draw(Monitor.gui)
            # self.drawGround()
            Monitor.gui.set_image(self.bgd_img)
            Monitor.gui.show()
        

monitor = Monitor()
monitor.draw()
