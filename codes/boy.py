# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import load_image, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT, SDLK_UP, draw_rectangle
import game_world
import game_framework

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP

def time_out(e):
    return e[0] == 'TIME_OUT'

PIXEL_PER_METER = (10.0 / 0.3)

RUN_SPEED_KMPH = 20.0
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


class Idle:

    @staticmethod
    def enter(boy, e):
        boy.action = 3

        if boy.face_dir == -1:
            boy.frame = 1
        elif boy.face_dir == 1:
            boy.frame = 5

        boy.dir = 0
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

        if boy.frame >= 4:
            boy.frame = 1

    @staticmethod
    def draw(boy):
        if boy.face_dir == -1:
            boy.image.clip_composite_draw(int(boy.frame) * 100, boy.action * 100, 100, 100, 0, '', boy.x, boy.y, 100, 100)

        elif boy.face_dir == 1:
            boy.image.clip_composite_draw(int(boy.frame) * 100, boy.action * 100, 100, 100, 0, 'h', boy.x, boy.y, 100, 100)


class Run:

    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            boy.dir, boy.action, boy.face_dir = 1, 2, 1
            boy.frame = 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            boy.dir, boy.action, boy.face_dir = -1, 2, -1
            boy.frame = 1

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

        if boy.frame >= 5:
            boy.frame = 1

        boy.x += boy.dir * RUN_SPEED_PPS * game_framework.frame_time
        boy.x = clamp(440, boy.x, 800-25)


    @staticmethod
    def draw(boy):
        if boy.face_dir == -1:
            boy.image.clip_composite_draw(int(boy.frame) * 100, boy.action * 100, 100, 100, 0, '', boy.x, boy.y, 100, 100)

        elif boy.face_dir == 1:
            boy.image.clip_composite_draw(int(boy.frame) * 100, boy.action * 100, 100, 100, 0, 'h', boy.x, boy.y, 100, 100)



class Jump:

    @staticmethod
    def enter(boy, e):
        boy.action = 0
        boy.frame = 1
        boy.dir = 1
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        if(boy.jump == 0 and boy.y <= 300):
            boy.dir = 1
            boy.y += boy.dir * JUMP_SPEED_PPS * game_framework.frame_time

        if(boy.jump == 0 and boy.y >= 300):
            boy.jump = 1

        if(boy.jump == 1 and boy.y >= 70):
            boy.dir = -1
            boy.y += boy.dir * JUMP_SPEED_PPS * game_framework.frame_time

        if(boy.jump == 1 and boy.y <= 70):
            boy.jump = 0
            boy.state_machine.handle_event(('TIME_OUT', 0))

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

        if boy.frame >= 3:
            boy.frame = 1


    @staticmethod
    def draw(boy):
        if boy.face_dir == -1:
            boy.image.clip_composite_draw(int(boy.frame) * 100, boy.action * 100, 100, 100, 0, '', boy.x, boy.y, 100, 100)
        else:
            boy.image.clip_composite_draw(int(boy.frame) * 100, boy.action * 100, 100, 100, 0, 'h', boy.x, boy.y, 100, 100)


class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, space_down: Jump},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Jump},
            Jump: {time_out: Idle}
        }

    def start(self):
        self.cur_state.enter(self.boy, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.boy)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy, e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.boy)





class Boy:
    def __init__(self):
        self.x, self.y = 600, 70
        self.frame = 0
        self.action = 3
        self.face_dir = -1
        self.dir = 0
        self.jump = 0
        self.score = 0
        self.image = load_image('character.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        if self.face_dir == -1:
            return self.x - 50, self.y - 30, self.x, self.y + 30
        else:
            return self.x, self.y - 30, self.x + 50, self.y + 30

    def handle_collision(self, group, other):
        pass
