import tkinter as tk
import time
from collections import deque

# ขนาดของแต่ละช่องในเขาวงกต
CELL_SIZE = 50
MOVE_DELAY = 300  # หน่วงเวลาให้เดินทีละช่อง (หน่วย: มิลลิวินาที)

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
        self.root.after(1000, self.auto_solve)  # เริ่มให้ AI เล่นเองหลังจาก 1 วินาที

    def load_level(self):
        self.maze = [list(row) for row in self.maps[self.current_level]]
        self.ply = self.find_position('P')
        self.end = self.find_position('E')

    def find_position(self, symbol):
        """ ค้นหาตำแหน่งของสัญลักษณ์ P หรือ E ในแผนที่ """
        for y, row in enumerate(self.maze):
            for x, val in enumerate(row):
                if val == symbol:
                    return Pos(y, x)
        return None

    def draw_maze(self):
        """ วาดเขาวงกตใหม่ทั้งหมด """
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
        """ ขยับตัวละครทีละช่องและอัปเดต UI """
        next_y, next_x = self.ply.y + dy, self.ply.x + dx
        if 0 <= next_y < len(self.maze) and 0 <= next_x < len(self.maze[0]):
            next_cell = self.maze[next_y][next_x]
            if next_cell in (' ', 'E'):
                self.maze[self.ply.y][self.ply.x] = ' '  # เคลียร์ตำแหน่งเดิม
                self.maze[next_y][next_x] = 'P'  # ย้ายไปตำแหน่งใหม่
                self.ply = Pos(next_y, next_x)
                self.draw_maze()  # วาดใหม่
                if next_cell == 'E':
                    self.root.after(1000, self.next_level)  # ไปด่านถัดไป

    def next_level(self):
        """ ไปยังด่านถัดไป """
        self.current_level += 1
        if self.current_level < len(self.maps):
            self.load_level()
            self.draw_maze()
            self.root.after(1000, self.auto_solve)  # เริ่มให้ AI เล่นอัตโนมัติ
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
        """ ใช้ BFS หาทางออกและเดินตามทางที่หาได้ """
        path = self.find_shortest_path()
        if path:
            self.follow_path(path)

    def find_shortest_path(self):
        """ ใช้ BFS หาเส้นทางที่สั้นที่สุดจาก P ไป E """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # ขึ้น, ลง, ซ้าย, ขวา
        queue = deque([(self.ply.y, self.ply.x, [])])  # (y, x, เส้นทางที่เดินมา)
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
        """ ให้ตัวละครเดินตามเส้นทางที่หาได้ทีละช่อง """
        def step(i):
            if i < len(path):
                dy, dx = path[i]
                self.move(dy, dx)
                self.root.after(MOVE_DELAY, step, i + 1)  # เดินทีละช่อง

        step(0)  # เริ่มเดิน

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
