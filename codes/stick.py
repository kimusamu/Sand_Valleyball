from pico2d import load_image, draw_rectangle


class Stick:
    def __init__(self):
        self.x = 400
        self.y = 150
        self.image = load_image('Stick.png')

    def draw(self):
        self.image.draw(400, 120)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - 5, self.y - 100, self.x + 5, self.y + 100

    def handle_collision(self, group, other):
        pass
