import sys
import random
import colorama
import termcolor

class Maze():
    PATH = 0  # 通路
    WALL = 1  # 壁

    def __init__(self, width, height):
        self.width = width    # 幅
        self.height = height  # 高さ
        self.maze = []        # 迷路の配列
        self.StartWall = []   # 壁の開始場所を持つリスト
        # 迷路は幅と高さ5以上の奇数で生成
        if (self.height < 5 or self.width < 5):
            print('迷路の幅と高さが5以上ではありません。')
            sys.exit()
        # 偶数なら1加える
        if (self.width % 2) == 0:
            self.width += 1
        if (self.height % 2) == 0:
            self.height += 1
        for x in range(0, self.width):
            row = []
            for y in range(0, self.height):
                if (x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1):
                    cell = self.WALL   # 壁にする
                else:
                    cell = self.PATH   # 通路にする
                    # xyとも偶数の場合は壁の開始場所として保持
                    if (x % 2 == 0 and y % 2 == 0):
                        self.StartWall.append([x, y])
                row.append(cell)
            self.maze.append(row)
        # スタートとゴールを入れる
        self.maze[1][0] = 'start'
        self.maze[width - 2][height - 1] = 'goal'

    # 迷路作成関数
    def make_maze(self):
        # 壁の拡張を開始できるセルがなくなるまで繰り返す
        while self.StartWall != []:
            # 開始セルをランダムに取得してリストからは削除
            x_start, y_start = self.StartWall.pop(random.randrange(0, len(self.StartWall)))
            # 選択候補が通路の場合は壁の拡張を開始する
            if self.maze[x_start][y_start] == self.PATH:
                self.CurrentWall = []  # 拡張中の壁情報を持つリスト
                self.extend_wall(x_start, y_start)
        return self.maze

    # 迷路拡張関数
    def extend_wall(self, x, y):
        Direction = []   # 壁を伸ばす方向
        # 通路かつその2つ先が現在拡張中の壁ではない
        if self.maze[x][y - 1] == self.PATH and [x, y - 2] not in self.CurrentWall:
            Direction.append('ue')
        if self.maze[x + 1][y] == self.PATH and [x + 2, y] not in self.CurrentWall:
            Direction.append('migi')
        if self.maze[x][y + 1] == self.PATH and [x, y + 2] not in self.CurrentWall:
            Direction.append('sita')
        if self.maze[x - 1][y] == self.PATH and [x - 2, y] not in self.CurrentWall:
            Direction.append('hidari')
        # 壁を伸ばせる方向がある場合
        if Direction != []:
            # まず現在地を壁にして拡張中の壁のリストに入れる
            self.maze[x][y] = self.WALL
            self.CurrentWall.append([x, y])
            direction = random.choice(Direction)   # 伸ばす方向をランダムに決定
            # 伸ばす2つ先の方向が通路の場合は既存の壁に到達できていないので、拡張を続ける判断のフラグ
            continue_make_wall = False
            # 伸ばした方向を壁(空欄3つ分)にする
            if direction == 'ue':
                continue_make_wall = (self.maze[x][y - 2] == self.PATH)
                self.maze[x][y - 1] = self.WALL
                self.maze[x][y - 2] = self.WALL
                self.CurrentWall.append([x, y - 2])
                if continue_make_wall:
                    self.extend_wall(x, y - 2)
            if direction == 'migi':
                continue_make_wall = (self.maze[x + 2][y] == self.PATH)
                self.maze[x + 1][y] = self.WALL
                self.maze[x + 2][y] = self.WALL
                self.CurrentWall.append([x + 2, y])
                if continue_make_wall:
                    self.extend_wall(x + 2, y)
            if direction == 'sita':
                continue_make_wall = (self.maze[x][y + 2] == self.PATH)
                self.maze[x][y + 1] = self.WALL
                self.maze[x][y + 2] = self.WALL
                self.CurrentWall.append([x, y + 2])
                if continue_make_wall:
                    self.extend_wall(x, y + 2)
            if direction == 'hidari':
                continue_make_wall = (self.maze[x - 2][y] == self.PATH)
                self.maze[x - 1][y] = self.WALL
                self.maze[x - 2][y] = self.WALL
                self.CurrentWall.append([x - 2, y])
                if continue_make_wall:
                    self.extend_wall(x - 2, y)
        else:
            previous_point_x, previous_point_y = self.CurrentWall.pop()
            self.extend_wall(previous_point_x, previous_point_y)

    # 迷路描画関数
    def print_maze(self):
        print(termcolor.colored('「START」から「GOAL」までの迷路を解け!!', 'cyan'))
        colorama.init()
        for row in self.maze:
            for cell in row:
                if cell == self.PATH:
                    print('   ', end='')   # 通路を表示
                elif cell == self.WALL:
                    print(termcolor.colored('   ', 'yellow', 'on_yellow'), end='')  # 壁を緑で表示
                elif cell == 'start':
                    print(termcolor.colored('START', 'blue'), end='')  # STARTを青で表示
                elif cell == 'goal':
                    print(termcolor.colored('GOAL', 'red'), end='')    # GOALを赤で表示
            print()

if __name__ == "__main__":
    # 挑戦者が迷路の大きさを設定
    print('作成する迷路の幅と高さを5以上の奇数に設定してください。')
    print('迷路の幅は？ > ')
    a = input()
    b = int(a)
    print('迷路の高さは？ > ')
    c = input()
    d = int(c)
    maze = Maze(b, d)  # 迷路の大きさ
    maze.make_maze()   # 迷路作成の関数
    maze.print_maze()  # 迷路描画の関数

