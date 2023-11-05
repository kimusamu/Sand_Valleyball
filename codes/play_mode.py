from pico2d import *
import game_framework

import game_world
from background import Desert_01, Desert_02, Desert_03
from codes import title_mode
from stick import Stick
from boy import Boy
from enemy import Enemy

# boy = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            boy.handle_event(event)
            enemy.handle_event(event)

def init():
    global desert_1
    global desert_2
    global desert_3
    global stick
    global boy
    global enemy

    running = True

    desert_1 = Desert_01()
    game_world.add_object(desert_1, 0)

    desert_2 = Desert_02()
    game_world.add_object(desert_2, 1)

    desert_3 = Desert_03()
    game_world.add_object(desert_3, 2)

    stick = Stick()
    game_world.add_object(stick, 3)

    boy = Boy()
    game_world.add_object(boy, 3)

    enemy = Enemy()
    game_world.add_object(enemy, 3)



def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    # delay(0.1)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

