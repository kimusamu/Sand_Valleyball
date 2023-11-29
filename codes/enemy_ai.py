from pico2d import *

import random
import math
import game_framework
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

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


class Enemy_AI:

    def __init__(self):
        self.x, self.y = 100, 70
        self.frame = 0
        self.action = 3
        self.face_dir = -1
        self.dir = 0
        self.jump = 0
        self.spike = 0
        self.spike_enemy_xy = 100
        self.spike_time = 0
        self.elapsed_time = 0
        self.image = load_image('character.png')
        self.AI_mode = 1

        self.tx, self.ty = 100, 70
        self.build_behavior_tree()

    def update(self):
        self.spike_time += game_framework.frame_time  # 경과 시간을 누적

        if self.spike_time >= 3:
            self.spike_enemy_xy = 100
            self.spike = 0
            self.spike_time = 0

        self.bt.run()

    def handle_event(self, event):
        pass

    def draw(self):
        if self.face_dir == -1:
            self.image.clip_composite_draw(int(self.frame) * 100, self.action * 100, 100, 100, 0, '', self.x, self.y, self.spike_enemy_xy, self.spike_enemy_xy)
        else:
            self.image.clip_composite_draw(int(self.frame) * 100, self.action * 100, 100, 100, 0, 'h', self.x, self.y, self.spike_enemy_xy, self.spike_enemy_xy)

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

    def set_random_location(self):
        self.tx, self.ty = random.randint(0, 400), 70
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = RUN_SPEED_PPS

        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time

    def move_to(self, r = 0.5):
        self.move_slightly_to(self.tx, self.ty)

        if (math.cos(self.dir) < 0):
            self.face_dir = -1
            self.action = 2
        else:
            self.face_dir = 1
            self.action = 2

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

        if self.frame >= 4:
            self.frame = 1

        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def is_ball_nearby(self, r):
        import codes
        if self.distance_less_than(codes.play_mode.ball.x, codes.play_mode.ball.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_ball(self, r=0.5):
        import codes
        self.move_slightly_to(codes.play_mode.ball.x, codes.play_mode.ball.y)
        self.x = clamp(25, self.x, 400 - 50)
        self.spike = 1

        if (math.cos(self.dir) < 0):
            self.face_dir = -1
            self.action = 2

        else:
            self.face_dir = 1
            self.action = 2

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

        if self.frame >= 4:
            self.frame = 1

        if self.distance_less_than(codes.play_mode.ball.x, codes.play_mode.ball.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        a1 = Action('Set target location', self.set_random_location)
        a2 = Action('Move to', self.move_to)
        SEQ_move_to_target_location = Sequence('Move to target location', a1, a2)

        c1 = Condition('공이 AI 주변에 있는가?', self.is_ball_nearby, 9)
        a3 = Action('공 주변으로 이동하여 공격한다', self.move_to_ball)
        SEQ_move_to_ball = Sequence('공 한테로 이동해서 공격한다', c1, a3)

        root = SEL_move_or_around = Selector('공한테 이동 혹은 주변 배회', SEQ_move_to_ball, SEQ_move_to_target_location)

        self.bt = BehaviorTree(root)