from pico2d import *
import game_world
from codes import game_framework


class Ball:
    image = None

    def __init__(self):
        Ball.image = load_image('Ball.png')
        self.x = 600
        self.y = 400
        self.velocity = 1
        self.jump = 0

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        if(self.jump == 0):
            self.y -= self.velocity * 5

        if(self.jump == 1):
            self.y += self.velocity * 5

        if(self.y >= 600):
            self.jump = 0

        if(self.y <= 70):
            self.y = 400

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def handle_collision(self, group, other):
        if group == 'boy:ball':
            self.jump = 1

        if group == 'enemy:ball':
            self.jump = 1