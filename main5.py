import pyxel
import random

TILE_WALL = 0
TILE_FLOOR = 1


# =========================
# ダンジョン生成
# =========================
class Dungeon:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.reset()
        self.generate()

    def reset(self):
        self.map = [[TILE_WALL for _ in range(self.w)] for _ in range(self.h)]
        self.rooms = []

        self.visible = [[False for _ in range(self.w)] for _ in range(self.h)]
        self.explored = [[False for _ in range(self.w)] for _ in range(self.h)]

    def generate(self, room_count=12):
        self.reset()
        self.generate_maze()
        self.add_rooms(room_count)
        self.connect_rooms()
        self.clean_isolated()

    def generate_maze(self):
        stack = [(1, 1)]
        self.map[1][1] = TILE_FLOOR

        while stack:
            x, y = stack[-1]
            dirs = [(2,0),(-2,0),(0,2),(0,-2)]
            random.shuffle(dirs)

            carved = False
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 1 <= nx < self.w-1 and 1 <= ny < self.h-1:
                    if self.map[ny][nx] == TILE_WALL:
                        self.map[y + dy//2][x + dx//2] = TILE_FLOOR
                        self.map[ny][nx] = TILE_FLOOR
                        stack.append((nx, ny))
                        carved = True
                        break

            if not carved:
                stack.pop()

    def is_overlapping(self, x, y, w, h, margin=1):
        for rx, ry, rw, rh in self.rooms:
            if (x < rx + rw + margin and
                x + w + margin > rx and
                y < ry + rh + margin and
                y + h + margin > ry):
                return True
        return False

    def add_rooms(self, count):
        attempts = 0
        max_attempts = count * 10

        while len(self.rooms) < count and attempts < max_attempts:
            attempts += 1

            rw = random.randint(4, 8)
            rh = random.randint(4, 8)
            rx = random.randint(1, self.w - rw - 2)
            ry = random.randint(1, self.h - rh - 2)

            if self.is_overlapping(rx, ry, rw, rh):
                continue

            for y in range(ry, ry + rh):
                for x in range(rx, rx + rw):
                    self.map[y][x] = TILE_FLOOR

            self.rooms.append((rx, ry, rw, rh))

            cx = rx + rw // 2
            cy = ry + rh // 2
            self.connect_to_maze(cx, cy)

    def connect_to_maze(self, x, y):
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            for i in range(1, 15):
                nx = x + dx*i
                ny = y + dy*i
                if not (0 <= nx < self.w and 0 <= ny < self.h):
                    break
                if self.map[ny][nx] == TILE_FLOOR:
                    for j in range(i):
                        self.map[y + dy*j][x + dx*j] = TILE_FLOOR
                    return

    def connect_rooms(self):
        for i in range(len(self.rooms) - 1):
            x1, y1, w1, h1 = self.rooms[i]
            x2, y2, w2, h2 = self.rooms[i+1]

            cx1, cy1 = x1 + w1//2, y1 + h1//2
            cx2, cy2 = x2 + w2//2, y2 + h2//2

            if random.random() < 0.5:
                self.h_corridor(cx1, cx2, cy1)
                self.v_corridor(cy1, cy2, cx2)
            else:
                self.v_corridor(cy1, cy2, cx1)
                self.h_corridor(cx1, cx2, cy2)

    def h_corridor(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.map[y][x] = TILE_FLOOR

    def v_corridor(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.map[y][x] = TILE_FLOOR

    def clean_isolated(self):
        for y in range(1, self.h - 1):
            for x in range(1, self.w - 1):
                if self.map[y][x] == TILE_FLOOR:
                    count = 0
                    for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                        if self.map[y+dy][x+dx] == TILE_FLOOR:
                            count += 1
                    if count <= 1:
                        self.map[y][x] = TILE_WALL

    def get_random_floor(self):
        while True:
            x = random.randint(1, self.w - 2)
            y = random.randint(1, self.h - 2)
            if self.map[y][x] == TILE_FLOOR:
                return x, y

    def update_fov(self, px, py, radius=6):
        for y in range(self.h):
            for x in range(self.w):
                dx = x - px
                dy = y - py
                dist = dx*dx + dy*dy

                if dist <= radius * radius:
                    self.visible[y][x] = True
                    self.explored[y][x] = True
                else:
                    self.visible[y][x] = False


# =========================
# アプリ
# =========================
class App:
    def __init__(self):
        self.tile = 16
        self.map_w = 64
        self.map_h = 64

        self.radius = 6
        self.view_w = self.radius * 2 + 1
        self.view_h = self.radius * 2 + 1

        self.minimap_tile = 1

        screen_w = self.view_w * self.tile + self.map_w * self.minimap_tile + 8
        screen_h = max(self.view_h * self.tile, self.map_h * self.minimap_tile)

        pyxel.init(screen_w, screen_h, title="Dungeon")

        self.dungeon = Dungeon(self.map_w, self.map_h)

        self.spawn_entities()
        self.dungeon.update_fov(self.player_x, self.player_y, self.radius)

        pyxel.run(self.update, self.draw)

    def spawn_entities(self):
        self.player_x, self.player_y = self.dungeon.get_random_floor()

        while True:
            self.goal_x, self.goal_y = self.dungeon.get_random_floor()
            if (self.goal_x, self.goal_y) != (self.player_x, self.player_y):
                break

    def try_move(self, dx, dy):
        nx = self.player_x + dx
        ny = self.player_y + dy

        if 0 <= nx < self.map_w and 0 <= ny < self.map_h:
            if self.dungeon.map[ny][nx] == TILE_FLOOR:
                self.player_x = nx
                self.player_y = ny

    def update(self):
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.try_move(-1, 0)
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            self.try_move(1, 0)
        elif pyxel.btnp(pyxel.KEY_UP):
            self.try_move(0, -1)
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.try_move(0, 1)

        if (self.player_x, self.player_y) == (self.goal_x, self.goal_y):
            self.dungeon.generate()
            self.spawn_entities()

        if pyxel.btnp(pyxel.KEY_R):
            self.dungeon.generate()
            self.spawn_entities()

        self.dungeon.update_fov(self.player_x, self.player_y)

    def draw(self):
        pyxel.cls(0)

        # -------- メインビュー --------
        cam_x = self.player_x - self.view_w // 2
        cam_y = self.player_y - self.view_h // 2

        cam_x = max(0, min(cam_x, self.map_w - self.view_w))
        cam_y = max(0, min(cam_y, self.map_h - self.view_h))

        for sy in range(self.view_h):
            for sx in range(self.view_w):
                mx = cam_x + sx
                my = cam_y + sy

                if not self.dungeon.explored[my][mx]:
                    col = 0
                elif not self.dungeon.visible[my][mx]:
                    continue
                else:
                    col = 7 if self.dungeon.map[my][mx] == TILE_FLOOR else 1

                pyxel.rect(sx*self.tile, sy*self.tile, self.tile, self.tile, col)

        # プレイヤー
        sx = self.player_x - cam_x
        sy = self.player_y - cam_y
        pyxel.rect(sx*self.tile, sy*self.tile, self.tile, self.tile, 8)

        # ゴール
        if self.dungeon.visible[self.goal_y][self.goal_x]:
            gx = self.goal_x - cam_x
            gy = self.goal_y - cam_y
            pyxel.rect(gx*self.tile, gy*self.tile, self.tile, self.tile, 11)

        # -------- ミニマップ --------
        offset_x = self.view_w * self.tile + 2
        offset_y = 4

        pyxel.rectb(offset_x - 1,
                    offset_y - 1,
                    self.map_w * self.minimap_tile + 2,
                    self.map_h * self.minimap_tile + 2,
                    7
                    )

        for y in range(self.map_h):
            for x in range(self.map_w):

                if not self.dungeon.explored[y][x]:
                    continue

                col = 1 if self.dungeon.map[y][x] == TILE_WALL else 5

                #if self.dungeon.visible[y][x]:
                #    col = 7

                px = offset_x + x * self.minimap_tile
                py = offset_y + y * self.minimap_tile
                pyxel.rect(px, py, self.minimap_tile, self.minimap_tile, col)

        cam_px = offset_x + cam_x * self.minimap_tile
        cam_py = offset_y + cam_y * self.minimap_tile

        cam_w = self.view_w * self.minimap_tile
        cam_h = self.view_h * self.minimap_tile

        pyxel.rectb(cam_px, cam_py, cam_w, cam_h, 8)

        # プレイヤー（ミニマップ）
        px = offset_x + self.player_x * self.minimap_tile
        py = offset_y + self.player_y * self.minimap_tile
        pyxel.rect(px, py, self.minimap_tile, self.minimap_tile, 8)

        # ゴール（ミニマップ）
        if self.dungeon.explored[self.goal_y][self.goal_x]:
            gx = offset_x + self.goal_x * self.minimap_tile
            gy = offset_y + self.goal_y * self.minimap_tile
            pyxel.rect(gx, gy, self.minimap_tile, self.minimap_tile, 11)


App()
