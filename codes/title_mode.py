import game_framework
from pico2d import load_image, delay, clear_canvas, update_canvas, get_events, get_time, SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDLK_a, SDLK_e
from codes import play_mode

mode = 1

def init():
    global image
    image = load_image('title.png')

def finish():
    global image
    del image


def handle_events():
    global mode
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
            game_framework.change_mode(play_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_e:
            game_framework.change_mode(play_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()


def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()


def update():
    pass
