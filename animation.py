import pyxel


class Animation:
    def __init__(self):
        pyxel.init(80, 60, title="pyxel animation")

        self.rabbit_y = 37
        self.rabbit_x = 10
        self.rabbit_color = 15
        self.rabbit_height = 10
        self.rabbit_vy = 0

        pyxel.run(self.update, self.draw)

    def draw_rabbit(self, x, y, color):
        pyxel.line(x + 2, y, x + 2, y + 2, color)
        pyxel.line(x + 4, y, x + 4, y + 4, color)
        pyxel.rect(x + 2, y + 3, 4, 3, color)
        pyxel.rect(x + 1, y + 6, 4, 3, color)
        pyxel.line(x , y + 9, x + 2, y + 9, color)
        pyxel.line(x + 4, y + 9, x + 5, y + 9, color)
    
        eye_color = 8 if color != 8 else 7
        pyxel.pset(x + 3, y + 4, eye_color)
        pyxel.pset(x + 5, y + 4, eye_color)

    def update(self):
        self.rabbit_y += self.rabbit_vy
        self.rabbit_vy += 0.1
        rabbit_bounce_y = pyxel.height - self.rabbit_height

        if self.rabbit_y >= rabbit_bounce_y:
            self.rabbit_y = rabbit_bounce_y
            self.rabbit_vy *= -0.95

    def draw(self):
        pyxel.cls(1)
        self.draw_rabbit(self.rabbit_x, self.rabbit_y, self.rabbit_color)


Animation()
