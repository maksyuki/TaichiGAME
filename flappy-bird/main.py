#!/usr/bin/env python
# -*- coding: utf-8 -*-
import taichi as ti
import random
import queue
from PIL import Image
import numpy as np

ti.init(arch=ti.gpu)

SCREEN_WIDTH = 288
SCREEN_HEIGH = 512

PIPE_GAP_SIZE = 50

FLOOR_HEIGH = 110
BASE_HEIGH = SCREEN_HEIGH - FLOOR_HEIGH

FPS = 60
GRAVITY_CONSTANT = -9.8 / 2
DELTA_UP_VEC = 2
DELTA_UP_VEC_LIMIT = 4

class Tool:
    def __init__(self):
        print("tool")

    def loadImg(self, path, reverse=False):
        if reverse:
            return np.array(Image.open(path).convert("RGB")).swapaxes(0, 1)
        else:
            return np.flip(np.array(Image.open(path).convert("RGB")).swapaxes(0, 1), axis=1)

class Bird(Tool):
    def __init__(self, pos):
        self.is_touch_boudary = False
        self.delta_time = FPS / 10000.0
        self.vec = 0
        self.pos = pos
        self.img = self.loadImg('./resources/yellowbird-midflap.png')


    def update(self):
        if self.pos[1] + self.img.shape[1] >= SCREEN_HEIGH or self.pos[1] < FLOOR_HEIGH:
            self.is_touch_boudary = True
            self.vec = 0
        else:
            self.vec += GRAVITY_CONSTANT * self.delta_time

        self.pos[1] += self.vec


    def up(self):
        self.vec += max(DELTA_UP_VEC_LIMIT, DELTA_UP_VEC)

    def down(self):
        print("down")

    def calcX(self):
        return self.pos[0]
    
    def calcY(self):
        return self.pos[1]

    def setX(self, val):
        self.pos[0] = val

    def setY(self, val):
        self.pos[1] = val
    
    def setVec(self, val):
        self.vec = val

class Pipe(Tool):
    def __init__(self, pos, heigh):
        self.pos = pos
        self.heigh = heigh
        self.vec = 10
        self.delta_time = FPS / 500.0
        self.bot_img = self.loadImg('./resources/pipe-green.png')
        self.top_img = self.loadImg('./resources/pipe-green.png', True)



    def update(self):
        self.pos[0] -= self.vec * self.delta_time
        

    def calcX(self):
        return self.pos[0]

    def calcY(self):
        return self.pos[1]


class RunState():
    IDLE1 = 0
    IDLE2 = 1
    RUNNING = 2
    OVER1 = 3
    OVER2 = 4
    
class Monitor(Tool):
    gui = ti.GUI("flappy bird", (SCREEN_WIDTH, SCREEN_HEIGH))
    # video_manager = ti.VideoManager(output_dir="./results", framerate=24, automatic_build=False)

    def __init__(self):
        self.state = RunState.IDLE1
        self.bird = Bird([0.3 * SCREEN_WIDTH, 0.5 * SCREEN_HEIGH])
        self.pipes = []
        self.pipes.append(Pipe([0.6 * SCREEN_WIDTH, FLOOR_HEIGH], self.genRandHeigh()))
        self.pipes.append(Pipe([1.5 * SCREEN_WIDTH, FLOOR_HEIGH], self.genRandHeigh()))

        self.bgd_img = self.loadImg('./resources/bgd-img-day.png')
        self.grd_img = self.loadImg('./resources/base.png')
        self.start_img = self.loadImg('./resources/message.png')
        self.gameover_img = self.loadImg('./resources/gameover.png')

        self.calcImg(self.bgd_img, self.grd_img)

    def calcImg(self, main_img, rel_img, x_offset = 0, y_offset = 0):
        width = min(main_img.shape[0], rel_img.shape[0]) # 
        heigh = min(main_img.shape[1], rel_img.shape[1])
        for i in range(width):
            for j in range(heigh):
                if(self.limitColor(rel_img[i,j][0]) and self.limitColor(rel_img[i,j][1])
                and self.limitColor(rel_img[i,j][2])):
                    main_img[x_offset+i, y_offset+j] = rel_img[i,j]


    def limitColor(self, val):
        return val > 0 and val <= 255


    def movePipe(self):
        for p in self.pipes:
            if p.pos[0] >= 0 and p.pos[0] < 10:
                p.pos[0] = 1 * SCREEN_WIDTH
                p.heigh = self.genRandHeigh()

    def genRandHeigh(self):
        return random.randint(FLOOR_HEIGH + 40, FLOOR_HEIGH + 140)

    def start(self):
        self.state = RunState.RUNNING

    def restart(self):
        self.state = RunState.IDLE1

    def drawScore(self):
        print("drawScore")

    def drawStartMenu(self):
        self.draw_img = self.bgd_img.copy()
        self.calcImg(self.draw_img, self.start_img, int((self.bgd_img.shape[0] - self.start_img.shape[0]) / 2),
        int((self.bgd_img.shape[1] - self.start_img.shape[1]) / 2))

    def drawGameOver(self):
        self.draw_img = self.bgd_img.copy()
        self.calcImg(self.draw_img, self.gameover_img, int((self.bgd_img.shape[0] - self.gameover_img.shape[0]) / 2),
        int((self.bgd_img.shape[1] - self.gameover_img.shape[1]) / 2))

    def drawGround(self):
        Monitor.gui.line([0, FLOOR_HEIGH / SCREEN_HEIGH], [1, FLOOR_HEIGH / SCREEN_HEIGH], color=0xffffff)

    def render(self):
        self.draw_img = self.bgd_img.copy()
        self.calcImg(self.draw_img, self.bird.img, int(self.bird.calcX()), int(self.bird.calcY()))
        # self.calcImg(self.draw_img, self.pipes[0].img, int(self.bird.calcX()), int(self.bird.calcY()))
        # self.calcImg(self.draw_img, self.pipes[0].bot_img, 80, 23)
        # self.calcImg(self.draw_img, self.pipes[0].top_img, 80, 150)
        # print(self.bird.calcX())
        # print(self.bird.calcY())
        


    def draw(self):
        while Monitor.gui.running:
            for e in Monitor.gui.get_events(ti.GUI.PRESS):
                if e.key == ti.GUI.ESCAPE:
                    exit()
                elif e.key == ti.GUI.UP:
                    print("press up key")
                    self.bird.up()
                elif e.key == ti.GUI.DOWN:
                    print("press down key start")
                    self.start()
                elif e.key == ti.GUI.LEFT:
                    print("press LEFT key restart")
                    self.restart()
                elif e.key == ti.GUI.RIGHT:
                    print("press right key")

            # for p in self.pipes:
            #     p.update()

            # self.movePipe()
            if self.state == RunState.IDLE1:
                self.state = RunState.IDLE2
                self.bird.setY(0.5 * SCREEN_HEIGH)
                self.bird.setVec(0)
                self.bird.is_touch_boudary = False
                self.drawStartMenu()

            elif self.state  == RunState.RUNNING:
                if self.bird.is_touch_boudary == False:
                    self.bird.update()
                    self.render()
                else:
                    self.state = RunState.OVER1
            elif self.state == RunState.OVER1:
                self.state = RunState.OVER2
                self.drawGameOver()

            # Monitor.video_manager.write_frame(self.draw_img)
            Monitor.gui.set_image(self.draw_img)
            Monitor.gui.show()


monitor = Monitor()
monitor.draw()
# Monitor.video_manager.make_video(gif=True, mp4=True)
# print(f'MP4 video is saved to {Monitor.video_manager.get_output_filename(".mp4")}')
# print(f'GIF video is saved to {Monitor.video_manager.get_output_filename(".gif")}')