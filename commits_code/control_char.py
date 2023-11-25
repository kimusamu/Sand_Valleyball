from pico2d import *

import game_world
from background import Desert_01, Desert_02, Desert_03
from stick import Stick
from boy import Boy

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            boy.handle_event(event)

def create_world():
    global running
    global background_1
    global background_2
    global background_3
    global char
    global stick

    running = True

    background_1 = Desert_01()
    game_world.add_object(background_1, 0)

    background_2 = Desert_02()
    game_world.add_object(background_2, 1)

    background_3 = Desert_03()
    game_world.add_object(background_3, 2)

    stick = Stick()
    game_world.add_object(stick, 3)

    char = Boy()
    game_world.add_object(char, 3)


def update_world():
    game_world.update()


def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()


open_canvas()
create_world()


while running:
    handle_events()
    game_world.update()
    clear_canvas()
    game_world.render()
    update_canvas()
    delay(0.01)


close_canvas()