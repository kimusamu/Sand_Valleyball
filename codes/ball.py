from pico2d import *
import game_world
import game_framework


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
        self.jump_speed = 5
        self.x_speed = 1
        self.elapsed_time = 0
        self.direction = 1

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        frame_time = game_framework.frame_time  # 현재 프레임 시간을 얻음
        self.elapsed_time += frame_time  # 경과 시간을 누적

        self.x += self.direction * self.velocity * self.x_speed

        if(self.jump == 0):
            if (self.right == 1):
                self.direction = 1

            elif (self.left == 1):
                self.direction = -1

            if self.elapsed_time >= 0.1:
                self.jump_speed += 1
                self.x_speed += 0.01
                self.elapsed_time = 0  # 경과 시간 초기화

            self.y -= self.velocity * self.jump_speed


        if(self.jump == 1):
            if (self.right == 1):
                self.direction = 1

            elif (self.left == 1):
                self.direction = -1

            if self.elapsed_time >= 0.1:
                self.jump_speed -= 1
                self.x_speed += 0.01
                self.elapsed_time = 0  # 경과 시간 초기화

            self.y += self.velocity * self.jump_speed

        if(self.x >= 800):
            if (self.right == 1):
                self.right = 0
                self.left = 1

            elif (self.left == 1):
                self.right = 1
                self.left = 0

        if (self.x <= 0):
            if (self.right == 1):
                self.right = 0
                self.left = 1

            elif (self.left == 1):
                self.right = 1
                self.left = 0

        if(self.y >= 600):
            self.jump = 0

        if(self.y <= 70):
            self.elapsed_time = 0
            self.jump_speed = 1
            self.x_speed = 1

            if(self.x < 400):
                self.right = 1
                self.left = 0
                self.x = 600
                self.y = 600

            elif(self.x >= 400):
                self.right = 0
                self.left = 1
                self.x = 200
                self.y = 600

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def handle_collision(self, group, other):
        if group == 'boy:ball':
            self.jump_speed = 5
            self.x_speed = 1
            self.elapsed_time = 0

            self.right = 0
            self.left = 1
            self.jump = 1

        if group == 'enemy:ball':
            self.jump_speed = 5
            self.x_speed = 1
            self.elapsed_time = 0

            self.right = 1
            self.left = 0
            self.jump = 1

        if group == 'stick:ball':
            self.jump_speed = 1
            self.x_speed = 1
            self.elapsed_time = 0

            if (self.right == 1):
                self.right = 0
                self.left = 1

            elif (self.left == 1):
                self.right = 1
                self.left = 0

            if(self.jump == 1):
                self.jump = 0

            if (self.jump == 0):
                self.jump = 1
