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
BASE_HEIGH = SCREEN_HEIGHT - FLOOR_HEIGH

class Bird():
    def __init__(self, pos):
    def update(self):
    def up(self):
    def down(self)
    def draw(self, gui)

class Pipe():
    def __init__(self, pos)
    def gen()
    def draw(self, gui)

class Monitor():
    def __init__(self)

    def drawScore(self)
    def drawGameOver(self)



