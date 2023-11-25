from pico2d import load_image

class Stick:
    def __init__(self):
        self.image = load_image('Stick.png')

    def draw(self):
        self.image.draw(400, 150)

    def update(self):
        pass
