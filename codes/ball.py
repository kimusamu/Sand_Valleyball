from pico2d import *
import game_world
from codes import game_framework


class Ball:
    image = None

    def __init__(self):
        Ball.image = load_image('Ball.png')
        self.x = 400
        self.y = 400
        self.velocity = 1

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.y -= self.velocity * 2

        if(self.y <= 70):
            self.y = 400

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20