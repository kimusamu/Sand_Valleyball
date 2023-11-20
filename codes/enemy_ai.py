from pico2d import *

import random
import math
import game_framework
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import play_mode

PIXEL_PER_METER = (10.0 / 0.3)

RUN_SPEED_KMPH = 40.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

JUMP_SPEED_KMPH = 60.0
JUMP_SPEED_MPM = (JUMP_SPEED_KMPH * 1000.0 / 60.0)
JUMP_SPEED_MPS = (JUMP_SPEED_MPM / 60.0)
JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6

class Enemy:
    def __init__(self):
        self.x, self.y = 100, 70
        self.frame = 0
        self.action = 3
        self.face_dir = -1
        self.dir = 0
        self.jump = 0
        self.score = 0
        self.spike = 0
        self.spike_enemy_xy = 100
        self.spike_time = 0
        self.image = load_image('character.png')

        self.tx = 100
        self.ty = 70
        self.build_behavior_tree()

    def update(self):
        frame_time = game_framework.frame_time  # 현재 프레임 시간을 얻음
        self.spike_time += frame_time  # 경과 시간을 누적

        if self.spike_time >= 3:
            self.spike_enemy_xy = 100
            self.spike = 0
            self.spike_time = 0

    def handle_event(self, event):
        pass
    def draw(self):
        if self.face_dir == -1:
            self.image.clip_composite_draw(int(self.frame) * 100, self.action * 100, 100, 100, 0, '', self.x, self.y, self.spike_enemy_xy, self.spike_enemy_xy)
        else:
            self.image.clip_composite_draw(int(self.frame) * 100, self.action * 100, 100, 100, 0, 'h', self.x, self.y, self.spike_enemy_xy, self.spike_enemy_xy)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        if self.face_dir == -1:
            return self.x - 50, self.y - 30, self.x, self.y + 30
        else:
            return self.x, self.y - 30, self.x + 50, self.y + 30

    def handle_collision(self, group, other):
        if group == 'enemy:ball':
            if (self.spike == 1):
                if self.spike_time >= 3:
                    self.spike_enemy_xy = 100
                    self.spike = 0
                    self.spike_time = 0

    def set_target_location(self, x=None, y=None):
        if not x or not y:
            raise ValueError('위치 지정을 해야 합니다.')
        self.tx, self.ty = x, y
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distanc2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distanc2 < (r * PIXEL_PER_METER) ** 2

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

    def is_ball_nearby(self, r):
        if self.distance_less_than(play_mode.ball.x, play_mode.ball.y, self.x, 70, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to(self, r=0.5):
        self.move_slightly_to(self.tx, 70)
        if self.distance_less_than(self.tx, 70, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def move_to_ball(self, r=0.5):
        self.move_slightly_to(play_mode.ball.x, play_mode.ball.y)
        if self.distance_less_than(play_mode.ball.x, play_mode.ball.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def set_random_location(self):
        self.tx = random.randint(0, 400)
        return BehaviorTree.SUCCESS


    def build_behavior_tree(self):
        ACT_move_ball =