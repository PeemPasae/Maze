import tkinter as tk
import time
from collections import deque

# ขนาดของแต่ละช่องในเขาวงกต
CELL_SIZE = 50

class Pos:
    def __init__(self, y, x):
        self.y = y
        self.x = x

class MazeGame:
    def __init__(self, root, maps):
        self.root = root
        self.maps = maps
        self.current_level = 0
        self.load_level()

        self.canvas = tk.Canvas(root, width=len(self.maze[0]) * CELL_SIZE, height=len(self.maze) * CELL_SIZE)
        self.canvas.pack()

        self.draw_maze()
        self.root.bind("<Up>", lambda event: self.move(-1, 0))
        self.root.bind("<Down>", lambda event: self.move(1, 0))
        self.root.bind("<Left>", lambda event: self.move(0, -1))
        self.root.bind("<Right>", lambda event: self.move(0, 1))
        self.root.bind("<space>", lambda event: self.auto_solve())  # กด Spacebar เพื่อให้ AI หาทางออกเอง

    def load_level(self):
        self.maze = [list(row) for row in self.maps[self.current_level]]
        self.ply = self.find_position('P')
        self.end = self.find_position('E')

    def find_position(self, symbol):
        for y, row in enumerate(self.maze):
            for x, val in enumerate(row):
                if val == symbol:
                    return Pos(y, x)
        return None

    def draw_maze(self):
        self.canvas.delete("all")
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                color = "white"
                if cell == "X":
                    color = "black"
                elif cell == "P":
                    color = "blue"
                elif cell == "E":
                    color = "green"
                self.canvas.create_rectangle(
                    x * CELL_SIZE, y * CELL_SIZE, 
                    (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, 
                    fill=color, outline="gray"
                )

    def move(self, dy, dx):
        next_y, next_x = self.ply.y + dy, self.ply.x + dx
        if 0 <= next_y < len(self.maze) and 0 <= next_x < len(self.maze[0]):
            next_cell = self.maze[next_y][next_x]
            if next_cell in (' ', 'E'):
                self.maze[self.ply.y][self.ply.x] = ' '
                self.maze[next_y][next_x] = 'P'
                self.ply = Pos(next_y, next_x)
                self.draw_maze()
                if next_cell == 'E':
                    self.next_level()

    def next_level(self):
        self.current_level += 1
        if self.current_level < len(self.maps):
            self.load_level()
            self.draw_maze()
        else:
            self.canvas.delete("all")
            self.canvas.create_text(
                len(self.maze[0]) * CELL_SIZE // 2,
                len(self.maze) * CELL_SIZE // 2,
                text="Congratulations! You Win!", 
                font=("Arial", 24),
                fill="red"
            )

    def auto_solve(self):
        """ ใช้ BFS เพื่อหาทางที่สั้นที่สุดจาก P ไป E """
        path = self.find_shortest_path()
        if path:
            self.follow_path(path)

    def find_shortest_path(self):
        """ ใช้ BFS หาเส้นทางที่สั้นที่สุด """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # ขึ้น, ลง, ซ้าย, ขวา
        queue = deque([(self.ply.y, self.ply.x, [])])  # (ตำแหน่ง y, ตำแหน่ง x, เส้นทางที่เดินมา)
        visited = set()
        
        while queue:
            y, x, path = queue.popleft()
            if (y, x) in visited:
                continue
            visited.add((y, x))

            if (y, x) == (self.end.y, self.end.x):
                return path  # คืนค่าเส้นทางที่สั้นที่สุด
            
            for dy, dx in directions:
                ny, nx = y + dy, x + dx
                if 0 <= ny < len(self.maze) and 0 <= nx < len(self.maze[0]) and self.maze[ny][nx] in (' ', 'E'):
                    queue.append((ny, nx, path + [(dy, dx)]))  # บันทึกเส้นทางที่เดินมา
        
        return None  # ถ้าไม่มีทางไปถึง `E`

    def follow_path(self, path):
        """ ให้ตัวละครเดินตามเส้นทางที่หาได้ """
        for dy, dx in path:
            self.move(dy, dx)
            self.root.update()  # อัปเดตหน้าจอ
            time.sleep(0.1)  # ทำให้ดูเหมือนเดินเอง

if __name__ == "__main__":
    maps = [
        [
            "XXXXXXXXXX",
            "XP       X",
            "X XXX XXX X",
            "X   X    X",
            "XXX X XXXX",
            "X   X   EX",
            "X XXXXXXXX",
            "X        X",
            "X XXXXXXXX",
            "XXXXXXXXXX"
        ],
        [
            "XXXXXXXXXX",
            "XP X     X",
            "X  X XXX X",
            "X  X   X X",
            "X  XXX X X",
            "X      X X",
            "X XXXX X X",
            "X X    X X",
            "X XXXXXX X",
            "X E      X",
            "XXXXXXXXXX"
        ],
        [
            "XXXXXXXXXX",
            "XP     X X",
            "XXXXXX X X",
            "X      X X",
            "X XXXX X X",
            "X X    X X",
            "X X XXXX X",
            "X X      X",
            "X XXXXXX X",
            "X E      X",
            "XXXXXXXXXX"
        ],
        [
            "XXXXXXXXXX",
            "XP X     X",
            "X  X XXX X",
            "X  X   X X",
            "X  XXX X X",
            "X      X X",
            "X XXXX X X",
            "X X    X X",
            "X XXXXXX X",
            "X E      X",
            "XXXXXXXXXX"
        ],
        [
            "XXXXXXXXXX",
            "XP       X",
            "X XXX X XX",
            "X   X X  X",
            "XXX X X XX",
            "X   X   EX",
            "X XXXXXXXX",
            "X   X    X",
            "X XXXXXXXXX",
            "XXXXXXXXXX"
        ]
    ]

    root = tk.Tk()
    root.title("Maze Game")
    game = MazeGame(root, maps)
    root.mainloop()
