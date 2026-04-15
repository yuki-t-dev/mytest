import pyxel

class App:
    def __init__(self):
        pyxel.init(90, 160)

        # ボール3個
        self.ball_x = [45, 30, 60]
        self.ball_y = [100, 60, 40]
        self.vx = [0, 0, 0]
        self.vy = [0, 0, 0]

        self.dragging = False
        self.start_x = 0
        self.start_y = 0

        # サウンド設定
        pyxel.sounds[0].set("c3", "p", "7", "n", 10)  # 壁
        pyxel.sounds[1].set("c4", "t", "7", "n", 10)  # ボール同士

        pyxel.run(self.update, self.draw)

    def update(self):
        radius = 3

        # --- タッチ処理（1個目だけ操作） ---
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.dragging = True
            self.start_x = pyxel.mouse_x
            self.start_y = pyxel.mouse_y

        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            if self.dragging:
                dx = pyxel.mouse_x - self.start_x
                dy = pyxel.mouse_y - self.start_y

                self.vx[0] = -dx * 0.1
                self.vy[0] = -dy * 0.1

            self.dragging = False

        # --- 全ボール処理 ---
        for i in range(3):

            # 壁反射（左右）
            if self.ball_x[i] < radius:
                self.ball_x[i] = radius
                self.vx[i] *= -1
                pyxel.play(0,0)

            if self.ball_x[i] > pyxel.width - radius:
                self.ball_x[i] = pyxel.width - radius
                self.vx[i] *= -1
                pyxel.play(0,0)

            # 壁反射（上下）
            if self.ball_y[i] < radius:
                self.ball_y[i] = radius
                self.vy[i] *= -1
                pyxel.play(0,0)

            if self.ball_y[i] > pyxel.height - radius:
                self.ball_y[i] = pyxel.height - radius
                self.vy[i] *= -1
                pyxel.play(0,0)

            # 移動
            self.ball_x[i] += self.vx[i]
            self.ball_y[i] += self.vy[i]

            # 減速
            self.vx[i] *= 0.985
            self.vy[i] *= 0.985

            # --- ボール同士の衝突（モンスト風） ---
        for i in range(3):
            for j in range(i + 1, 3):
                dx = self.ball_x[i] - self.ball_x[j]
                dy = self.ball_y[i] - self.ball_y[j]
                dist_sq = dx * dx + dy * dy
                min_dist = 6

                if dist_sq < min_dist * min_dist:
                    dist = dist_sq ** 0.5
                    if dist == 0:
                        continue

            # 法線ベクトル（当たった方向）
                    nx = dx / dist
                    ny = dy / dist

            # 相対速度
                    rvx = self.vx[i] - self.vx[j]
                    rvy = self.vy[i] - self.vy[j]

            # 法線方向の速度成分
                    dot = rvx * nx + rvy * ny

            # 離れてるなら何もしない
                    if dot > 0:
                        continue

            # 反発（ここがキモ）
                    self.vx[i] -= dot * nx
                    self.vy[i] -= dot * ny
                    self.vx[j] += dot * nx
                    self.vy[j] += dot * ny

                    pyxel.play(1, 1)

            # めり込み防止
                    overlap = min_dist - dist
                    self.ball_x[i] += nx * overlap / 2
                    self.ball_y[i] += ny * overlap / 2
                    self.ball_x[j] -= nx * overlap / 2
                    self.ball_y[j] -= ny * overlap / 2

#        if abs(self.vx[i]) < 0.10:
#            self.vx[i] = 0
#        if abs(self.vy[i]) < 0.10:
#            self.vy[i] = 0

    def draw(self):
        pyxel.cls(0)

        # ボール描画
        for i in range(3):
            pyxel.circ(self.ball_x[i], self.ball_y[i], 3, 7+i)

        # 引っ張り線（1個目）
        if self.dragging:
            pyxel.line(
                self.ball_x[0], self.ball_y[0],
                pyxel.mouse_x, pyxel.mouse_y,
                10
            )

App()
