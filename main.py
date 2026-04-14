import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120)

        self.ball_x = 80
        self.ball_y = 60
        self.vx = 0
        self.vy = 0

        self.dragging = False
        self.start_x = 0
        self.start_y = 0

        pyxel.run(self.update, self.draw)

    def update(self):

        # 壁反射
        radius = 3  # ボールの半径

        # 左右
        if self.ball_x < radius:
            self.ball_x = radius
            self.vx *= -1

        if self.ball_x > pyxel.width - radius:
            self.ball_x = pyxel.width - radius
            self.vx *= -1

        # 上下
        if self.ball_y < radius:
            self.ball_y = radius
            self.vy *= -1

        if self.ball_y > pyxel.height - radius:
            self.ball_y = pyxel.height - radius
            self.vy *= -1

        # タッチ開始
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.dragging = True
            self.start_x = pyxel.mouse_x
            self.start_y = pyxel.mouse_y

        # タッチ終了（ここで発射！）
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            if self.dragging:
                dx = pyxel.mouse_x - self.start_x
                dy = pyxel.mouse_y - self.start_y

                # 逆方向に飛ばす（モンスト式）
                self.vx = -dx * 0.1
                self.vy = -dy * 0.1

            self.dragging = False

        # 移動
        self.ball_x += self.vx
        self.ball_y += self.vy

        # 減速（摩擦）
        self.vx *= 0.98
        self.vy *= 0.98

    def draw(self):
        pyxel.cls(0)

        # ボール
        pyxel.circ(self.ball_x, self.ball_y, 3, 7)

        # 引っ張り線
        if self.dragging:
            pyxel.line(
                self.ball_x, self.ball_y,
                pyxel.mouse_x, pyxel.mouse_y,
                8
            )

App()
