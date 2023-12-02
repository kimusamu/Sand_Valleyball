from pico2d import load_image, draw_rectangle, load_music


class Desert_01:
    def __init__(self):
        self.image = load_image('Desert_01.png')
        self.bgm = load_music('game_sound.mp3')
        self.bgm.set_volume(20)
        self.bgm.repeat_play()

    def draw(self):
        self.image.draw(400, 300)

    def update(self):
        pass


class Desert_02:
    def __init__(self):
        self.image = load_image('Desert_02.png')

    def draw(self):
        self.image.draw(400, 300)

    def update(self):
        pass


class Desert_03:
    def __init__(self):
        self.x = 400
        self.y = 10
        self.image = load_image('Desert_03.png')

    def draw(self):
        self.image.draw(400, 10)

    def update(self):
        pass

