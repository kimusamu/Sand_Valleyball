from pico2d import *
import game_framework
from codes import win_1_mode, win_2_mode, win_3_mode, win_4_mode, boy, enemy, enemy_ai
import game_world

class Ball:
    image = None
    enemy_ball_sound = None
    boy_ball_sound = None
    stick_ball_sound = None

    def __init__(self):
        if Ball.image == None:
            self.image = load_image('Ball.png')
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
        self.font = load_font('ENCR10B.TTF', 40)
        self.boy_score = 0
        self.enemy_score = 0
        self.AI_switch = 0

        if not Ball.enemy_ball_sound:
            Ball.enemy_ball_sound = load_wav('ball_sound.wav')
            Ball.boy_ball_sound = load_wav('ball_sound.wav')
            Ball.stick_ball_sound = load_wav('ball_sound.wav')
            Ball.enemy_ball_sound.set_volume(50)
            Ball.boy_ball_sound.set_volume(50)
            Ball.stick_ball_sound.set_volume(50)

    def draw(self):
        self.image.draw(self.x, self.y)
        self.font.draw(150, 500, f'{self.boy_score}', (0, 0, 255))
        self.font.draw(600, 500, f'{self.enemy_score}', (0, 0, 255))

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
            self.right = 0
            self.left = 1

        if (self.x <= 0):
            self.right = 1
            self.left = 0

        if(self.y >= 600):
            self.jump = 0

        if(self.y <= 70):
            self.jump_speed = 5
            self.x_speed = 1
            self.elapsed_time = 0
            self.velocity = 0.5

            if(self.x < 400):
                self.enemy_score += 1
                self.right = 0
                self.left = 1
                self.x = 200
                self.y = 600

            elif(self.x >= 400):
                self.boy_score += 1
                self.right = 0
                self.left = 1
                self.x = 600
                self.y = 600

        if self.enemy_score == 10 and self.AI_switch == 0:
            boy.x = 600
            boy.y = 70
            enemy.x = 100
            enemy.y = 70
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
            game_framework.change_mode(win_1_mode)

        elif self.boy_score == 10 and self.AI_switch == 0:
            boy.x = 600
            boy.y = 70
            enemy.x = 100
            enemy.y = 70
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
            game_framework.change_mode(win_3_mode)

        elif self.enemy_score == 10 and self.AI_switch == 1:
            boy.x = 600
            boy.y = 70
            enemy_ai.x = 100
            enemy_ai.y = 70
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
            game_framework.change_mode(win_2_mode)

        elif self.boy_score == 10 and self.AI_switch == 1:
            boy.x = 600
            boy.y = 70
            enemy_ai.x = 100
            enemy_ai.y = 70
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
            game_framework.change_mode(win_4_mode)


    def get_bb_1(self):
        return self.x - 7, self.y - 22, self.x + 7, self.y + 22
    def get_bb_2(self):
        return self.x - 11, self.y - 19, self.x + 11, self.y + 19
    def get_bb_3(self):
        return self.x - 13, self.y - 16, self.x + 13, self.y + 16
    def get_bb_4(self):
        return self.x - 16, self.y - 13, self.x + 16, self.y + 13
    def get_bb_5(self):
        return self.x - 19, self.y - 11, self.x + 19, self.y + 11
    def get_bb_6(self):
        return self.x - 22, self.y - 7, self.x + 22, self.y + 7

    def handle_collision(self, group, other):
        if group == 'boy:ball':
            Ball.boy_ball_sound.play()

            if (other.spike == 1):
                self.jump_speed = 5
                self.x_speed = 3
                self.elapsed_time = 0
                self.velocity = 3

            else:
                self.jump_speed = 5
                self.x_speed = 1
                self.elapsed_time = 0
                self.velocity = 1

            if(other.face_dir == -1):
                self.right = 0
                self.left = 1

            elif(other.face_dir == 1):
                self.right = 1
                self.left = 0

            self.jump = 1



        if group == 'enemy:ball':
            Ball.enemy_ball_sound.play()

            if(other.spike == 1 and self.jump == 1 and other.AI_mode == 0):
                self.AI_switch = 0
                self.jump_speed = 5
                self.x_speed = 3
                self.elapsed_time = 0
                self.velocity = 3

            elif (other.spike == 1 and self.jump == 1 and other.AI_mode == 1):
                self.AI_switch = 1
                self.jump_speed = 5
                self.x_speed = 3
                self.elapsed_time = 0
                self.velocity = 3

            else:
                self.jump_speed = 5
                self.x_speed = 1
                self.elapsed_time = 0
                self.velocity = 1

            if (other.face_dir == -1):
                self.right = 0
                self.left = 1

            elif (other.face_dir == 1):
                self.right = 1
                self.left = 0

            self.jump = 1


        if group == 'stick:ball':
            Ball.stick_ball_sound.play()

            self.jump_speed = 5
            self.x_speed = 1
            self.elapsed_time = 0
            self.velocity = 1

            if (self.right == 1):
                self.right = 0
                self.left = 1

            if (self.left == 1):
                self.right = 1
                self.left = 0

            if (self.jump == 1):
                self.jump = 0

            if (self.jump == 0):
                self.jump = 1
