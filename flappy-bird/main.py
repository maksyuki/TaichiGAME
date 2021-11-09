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

PIPE_GAP_SIZE = 200

FLOOR_HEIGH = 110
BASE_HEIGH = SCREEN_HEIGH - FLOOR_HEIGH

FPS = 60
GRAVITY_CONSTANT = -9.8 * 1.2
DELTA_UP_VEC = 2
DELTA_UP_VEC_LIMIT = 2.5

class Bird():
    def __init__(self, pos):
        self.is_touch_boudary = False
        self.delta_time = FPS / 10000.0
        self.vec = 0
        self.pos = pos
        self.img_cnt = 0
        self.img = []
        # self.img = Image.open('./resources/yellowbird-upflap.png').convert("RGBA")
        self.img.append(Image.open('./resources/yellowbird-upflap.png').convert("RGBA"))
        self.img.append(Image.open('./resources/yellowbird-midflap.png').convert("RGBA"))
        self.img.append(Image.open('./resources/yellowbird-downflap.png').convert("RGBA"))

    def initState(self, main_img):
        self.setY(main_img, 0.5 * SCREEN_HEIGH)
        self.setVec(0)
        self.is_touch_boudary = False

    def update(self):
        self.img_cnt = (self.img_cnt + 1) % 3
        if self.pos[1] + self.img[0].size[1] >= SCREEN_HEIGH or self.pos[1] < FLOOR_HEIGH:
            self.is_touch_boudary = True
            self.vec = 0
        else:
            self.vec += GRAVITY_CONSTANT * self.delta_time

        self.pos[1] += self.vec


    def up(self):
        self.vec += max(DELTA_UP_VEC_LIMIT, DELTA_UP_VEC)

    def calcX(self):
        return self.pos[0]
    
    def calcY(self, main_img):
        return self.pos[1]

    def setX(self, val):
        self.pos[0] = val

    def setY(self, main_img, val):
        self.pos[1] = val
    
    def setVec(self, val):
        self.vec = val

class Ground():
    def __init__(self):
        self.vec = 10
        self.delta_time = FPS / 500.0
        self.img = Image.open('./resources/base.png').convert("RGBA")

class Pipe():
    def __init__(self, pos, heigh):
        self.pos = pos
        self.heigh = heigh
        self.vec = 10
        self.delta_time = FPS / 500.0
        self.bot_img = Image.open('./resources/pipe-green.png').convert("RGBA")
        self.top_img = Image.open('./resources/pipe-green.png').convert("RGBA")


    def update(self):
        self.pos[0] -= self.vec * self.delta_time
        

    def calcX(self):
        return self.pos[0]

    def calcY(self):
        return self.pos[1]

    def setX(self, val):
        self.pos[0] = val

class RunState():
    IDLE1 = 0
    IDLE2 = 1
    RUNNING = 2
    OVER1 = 3
    OVER2 = 4

class Monitor():
    gui = ti.GUI("flappy bird", (SCREEN_WIDTH, SCREEN_HEIGH))
    # video_manager = ti.VideoManager(output_dir="./results", framerate=24, automatic_build=False)

    def __init__(self):
        self.state = RunState.IDLE1
        self.bird = Bird([0.3 * SCREEN_WIDTH, 0.5 * SCREEN_HEIGH])
        self.ground = Ground()
        self.pipes = []
        self.pipes.append(Pipe([0.9 * SCREEN_WIDTH, FLOOR_HEIGH], self.genRandHeigh()))
        # self.pipes.append(Pipe([1 * SCREEN_WIDTH, FLOOR_HEIGH], self.genRandHeigh()))

        self.initState()
        self.bgd_img = Image.open('./resources/bgd-img-day.png').convert("RGBA")
        self.start_img = Image.open('./resources/message.png').convert("RGBA")
        self.gameover_img = Image.open('./resources/gameover.png').convert("RGBA")
        self.score_img = []
        self.score_img.append(Image.open('./resources/0.png').convert("RGBA"))
        self.score_img.append(Image.open('./resources/1.png').convert("RGBA"))
        self.score_img.append(Image.open('./resources/2.png').convert("RGBA"))
        self.score_img.append(Image.open('./resources/3.png').convert("RGBA"))
        self.score_img.append(Image.open('./resources/4.png').convert("RGBA"))
        self.score_img.append(Image.open('./resources/5.png').convert("RGBA"))
        self.score_img.append(Image.open('./resources/6.png').convert("RGBA"))
        self.score_img.append(Image.open('./resources/7.png').convert("RGBA"))
        self.score_img.append(Image.open('./resources/8.png').convert("RGBA"))
        self.score_img.append(Image.open('./resources/9.png').convert("RGBA"))

    def initState(self):
        self.score = 0
        self.score_iter = False
        self.is_collision = False
        self.pipes[0].setX(0.9 * SCREEN_WIDTH)
        self.pipes[0].heigh = self.genRandHeigh()

    def calcImg(self, main_img, rel_img, x_offset=0, y_offset=0, rotate=False):
        # (max(x_off, 0), min(y_off+rel.heigh, main.heigh)) (min(x_off+rel.width, main.width), max(y_off, 0))
        # ===> 
        # (max(x_off, 0), main.heigh - min(y_off+rel.heigh, main.heigh)) 
        # (min(x_off+rel.width, main.width), main.heigh - max(y_off, 0))
        ori_y1 = min(y_offset+rel_img.size[1], main_img.size[1])
        ori_y2 = max(y_offset, 0)
        x1 = max(x_offset, 0)
        x2 = min(x_offset+rel_img.size[0], main_img.size[0])
        y1 = main_img.size[1] - ori_y1
        y2 = main_img.size[1] - ori_y2

        box1 = (x1, y1, x2, y2)
        box2 = (x1-x_offset, rel_img.size[1]-(ori_y1-y_offset), x2-x_offset, rel_img.size[1]-(ori_y2-y_offset))

        # print(box1)
        # print(main_img.size)
        # print(box2)
        # print(rel_img.size)
        tmp_img1 = main_img.crop(box1)
        if rotate:
            rel_img = rel_img.transpose(method=Image.ROTATE_180)
        tmp_img2 = rel_img.crop(box2)
        tmp_img1 = Image.alpha_composite(tmp_img1, tmp_img2)
        main_img.paste(tmp_img1, box1)

    def movePipe(self):
        for p in self.pipes:
            if p.pos[0] >= 0 and p.pos[0] < 10:
                p.pos[0] = 1 * SCREEN_WIDTH
                p.heigh = self.genRandHeigh()
                self.score_iter = False

    def genRandHeigh(self):
        return random.randint(0, 200) - 100 #[-100, 100]

    def geoIntersectCheck(self, pipe):
        bird_center_x = self.bird.pos[0] + self.bird.img[0].size[0] / 3.0
        bird_center_y = self.bird.pos[1] + self.bird.img[0].size[1] / 3.0
        pipe_center_x = pipe.pos[0] + pipe.bot_img.size[0] / 2.0
        pipe_center_y = pipe.pos[1] + pipe.bot_img.size[1] / 2.0

        # print(abs(bird_center_x - pipe_center_x))
        # print(abs(self.bird.img.size[0] + pipe.bot_img.size[0]) / 2.0)
        # print(abs(bird_center_y - pipe_center_y))
        # print(abs(self.bird.img.size[1] + pipe.bot_img.size[1]) / 2.0)

        if ((abs(bird_center_x - pipe_center_x) < abs(self.bird.img[0].size[0] + pipe.bot_img.size[0]) / 2.0) and
           (abs(bird_center_y - pipe_center_y) < abs(self.bird.img[0].size[1] + pipe.bot_img.size[1]) / 2.0)):
            return True
        else:
            return False

    def collisionCheck(self):
        for p in self.pipes:
            # if self.geoIntersectCheck(p):
            #     self.is_collision = True
            #     return

            if p.pos[0] + p.bot_img.size[0] < self.bird.pos[0] and self.score_iter == False:
                self.score = self.score + 1
                self.score_iter = True

    def start(self):
        self.state = RunState.RUNNING

    def restart(self):
        self.state = RunState.IDLE1

    def drawScore(self, main_img):
        idx = self.score % 10
        self.calcImg(main_img, self.score_img[idx], int((self.bgd_img.size[0] - self.score_img[idx].size[0]) / 2),
        int((self.bgd_img.size[1]-self.score_img[idx].size[1])/2)+150)

    def drawStartMenu(self):
        self.draw_img = self.bgd_img.copy()
        self.calcImg(self.draw_img, self.start_img, int((self.bgd_img.size[0]-self.start_img.size[0])/2),
        int((self.bgd_img.size[1]-self.start_img.size[1])/2))

    def drawGameOver(self):
        self.draw_img = self.bgd_img.copy()
        self.calcImg(self.draw_img, self.gameover_img, int((self.bgd_img.size[0]-self.gameover_img.size[0])/2),
        int((self.bgd_img.size[1] - self.gameover_img.size[1])/2))

    def render(self):
        self.draw_img = self.bgd_img.copy()
        self.calcImg(self.draw_img, self.pipes[0].bot_img, int(self.pipes[0].pos[0]), -100+self.pipes[0].heigh)
        self.calcImg(self.draw_img, self.pipes[0].top_img, int(self.pipes[0].pos[0]), 300+self.pipes[0].heigh, True)
        self.calcImg(self.draw_img, self.bird.img[self.bird.img_cnt], int(self.bird.calcX()), int(self.bird.calcY(self.bgd_img)))
        self.calcImg(self.draw_img, self.ground.img)
        self.drawScore(self.draw_img)
        print(self.bird.calcX())
        print(self.bird.calcY(self.bgd_img))
        

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

            if self.state == RunState.IDLE1:
                self.state = RunState.IDLE2
                self.bird.initState(self.bgd_img)
                self.initState()
                self.drawStartMenu()

            elif self.state  == RunState.RUNNING:
                if self.bird.is_touch_boudary == False and self.is_collision == False:
                    self.bird.update()
                    for p in self.pipes:
                        p.update()

                    self.render()
                else:
                    self.state = RunState.OVER1
            elif self.state == RunState.OVER1:
                self.state = RunState.OVER2
                self.drawGameOver()

            self.movePipe()
            self.collisionCheck()
            # Monitor.video_manager.write_frame(self.draw_img)
            Monitor.gui.set_image(np.flip(np.array(self.draw_img.convert("RGB")).swapaxes(0, 1), axis=1))
            Monitor.gui.show()


monitor = Monitor()
monitor.draw()

# Monitor.video_manager.make_video(gif=True, mp4=True)
# print(f'MP4 video is saved to {Monitor.video_manager.get_output_filename(".mp4")}')
# print(f'GIF video is saved to {Monitor.video_manager.get_output_filename(".gif")}')