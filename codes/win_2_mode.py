import game_framework
from pico2d import load_image, clear_canvas, update_canvas, get_events, SDL_KEYDOWN, SDLK_ESCAPE
from codes import title_mode


def init():
    global image
    image = load_image('win_image_2.png')

def finish():
    global image
    del image


def handle_events():
    global mode
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)


def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()


def update():
    pass
