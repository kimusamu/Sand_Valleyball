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
        self.left = 1
        self.right = 0
        self.jump = 0

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        if(self.jump == 0):
            if (self.right == 1):
                self.x += self.velocity * 0.7

            elif (self.left == 1):
                self.x -= self.velocity * 0.7

            self.y -= self.velocity * 5

        if(self.jump == 1):
            if (self.right == 1):
                self.x += self.velocity * 0.7

            elif (self.left == 1):
                self.x -= self.velocity * 0.7

            self.y += self.velocity * 5

        if(self.y >= 600):
            self.jump = 0

        if(self.y <= 70):
            if(self.x >= 0 and self.x < 400):
                self.right = 1
                self.left = 0
                self.x = 600
                self.y = 400

            elif(self.x >= 400 and self.x < 800):
                self.right = 0
                self.left = 1
                self.x = 200
                self.y = 400

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def handle_collision(self, group, other):
        if group == 'boy:ball':
            self.right = 0
            self.left = 1
            self.jump = 1

        if group == 'enemy:ball':
            self.right = 1
            self.left = 0
            self.jump = 1