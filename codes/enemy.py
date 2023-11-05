from pico2d import load_image, clamp,  SDL_KEYDOWN, SDL_KEYUP, SDLK_a, SDLK_d, SDLK_w
import game_world
import game_framework

# state event check
# ( state event type, event value )

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w

def time_out(e):
    return e[0] == 'TIME_OUT'

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6


class Idle:

    @staticmethod
    def enter(enemy, e):
        enemy.action = 3

        if enemy.face_dir == -1:
            enemy.frame = 1
        elif enemy.face_dir == 1:
            enemy.frame = 5

        enemy.dir = 0
        pass

    @staticmethod
    def exit(enemy, e):
        pass

    @staticmethod
    def do(enemy):
        enemy.frame = (enemy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

        if enemy.frame >= 4:
            enemy.frame = 1

    @staticmethod
    def draw(enemy):
        if enemy.face_dir == -1:
            enemy.image.clip_composite_draw(int(enemy.frame) * 100, enemy.action * 100, 100, 100, 0, '', enemy.x, enemy.y, 100, 100)

        elif enemy.face_dir == 1:
            enemy.image.clip_composite_draw(int(enemy.frame) * 100, enemy.action * 100, 100, 100, 0, 'h', enemy.x, enemy.y, 100, 100)


class Run:

    @staticmethod
    def enter(enemy, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            enemy.dir, enemy.action, enemy.face_dir = 1, 2, 1
            enemy.frame = 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            enemy.dir, enemy.action, enemy.face_dir = -1, 2, -1
            enemy.frame = 1

    @staticmethod
    def exit(enemy, e):
        pass

    @staticmethod
    def do(enemy):
        enemy.frame = (enemy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

        if enemy.frame >= 5:
            enemy.frame = 1

        enemy.x += enemy.dir * RUN_SPEED_PPS * game_framework.frame_time
        enemy.x = clamp(25, enemy.x, 400-40)


    @staticmethod
    def draw(enemy):
        if enemy.face_dir == -1:
            enemy.image.clip_composite_draw(int(enemy.frame) * 100, enemy.action * 100, 100, 100, 0, '', enemy.x, enemy.y, 100, 100)

        elif enemy.face_dir == 1:
            enemy.image.clip_composite_draw(int(enemy.frame) * 100, enemy.action * 100, 100, 100, 0, 'h', enemy.x, enemy.y, 100, 100)



class Sleep:

    @staticmethod
    def enter(enemy, e):
        enemy.action = 0
        enemy.frame = 1
        enemy.dir = 1
        pass

    @staticmethod
    def exit(enemy, e):
        pass

    @staticmethod
    def do(enemy):
        if(enemy.jump == 0 and enemy.y <= 300):
            enemy.dir = 1
            enemy.y += enemy.dir * RUN_SPEED_PPS * game_framework.frame_time

        if(enemy.jump == 0 and enemy.y >= 300):
            enemy.jump = 1

        if(enemy.jump == 1 and enemy.y >= 70):
            enemy.dir = -1
            enemy.y += enemy.dir * RUN_SPEED_PPS * game_framework.frame_time

        if(enemy.jump == 1 and enemy.y <= 70):
            enemy.jump = 0
            enemy.state_machine.handle_event(('TIME_OUT', 0))

        enemy.frame = (enemy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

        if enemy.frame >= 3:
            enemy.frame = 1


    @staticmethod
    def draw(boy):
        if boy.face_dir == -1:
            boy.image.clip_composite_draw(int(boy.frame) * 100, boy.action * 100, 100, 100, 0, '', boy.x, boy.y, 100, 100)
        else:
            boy.image.clip_composite_draw(int(boy.frame) * 100, boy.action * 100, 100, 100, 0, 'h', boy.x, boy.y, 100, 100)


class StateMachine:
    def __init__(self, enemy):
        self.enemy = enemy
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, space_down: Sleep},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Sleep},
            Sleep: {time_out: Idle}
        }

    def start(self):
        self.cur_state.enter(self.enemy, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.enemy)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.enemy, e)
                self.cur_state = next_state
                self.cur_state.enter(self.enemy, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.enemy)





class Enemy:
    def __init__(self):
        self.x, self.y = 100, 70
        self.frame = 0
        self.action = 3
        self.face_dir = -1
        self.dir = 0
        self.jump = 0
        self.image = load_image('character.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
