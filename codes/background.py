from pico2d import load_image, draw_rectangle


class Desert_01:
    def __init__(self):
        self.image = load_image('Desert_01.png')

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
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - 400, self.y, self.x + 400, self.y + 50

