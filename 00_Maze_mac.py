import os
import time

class maze:
    def __init__(self) -> None:
        self.maze = [
                    ["X", "X", "X", "X", "X", "X", "X"],
                    ["X", " ", " ", " ", "X", " ", "X"],
                    ["X", " ", "X", " ", "X", " ", " "],
                    ["X", " ", "X", " ", "X", " ", "X"],
                    ["X", " ", "X", " ", " ", " ", "X"],
                    ["X", " ", "X", "X", "X", "X", "X"],
                    ]
        self.ply = pos(5, 1)
        self.end = pos(2, 6)
        self.maze[self.ply.y][self.ply.x] = "P"
        self.maze[self.end.y][self.end.x] = "E"

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")  # ใช้คำสั่งที่เหมาะกับ OS 
    def isInBound(self, y, x):
        return 0 <= y < len(self.maze) and 0 <= x < len(self.maze[0])

    def print(self):
        self.clear_screen()
        print("\n\n\n")
        for row in self.maze:
            print(" ".join(row))  # ปรับโค้ดให้สั้นลง
        print("\n\n\n")

    def printEND(self):
        self.clear_screen()
        print("\n\n\n")
        print(">>>>> Congraturation!!! <<<<<")
        print("\n\n\n")

    def move(self, dy, dx):
        next_move = pos(self.ply.y + dy, self.ply.x + dx)
        if self.isInBound(next_move.y, next_move.x):
            if self.maze[next_move.y][next_move.x] == " ":
                self.maze[self.ply.y][self.ply.x] = " "
                self.maze[next_move.y][next_move.x] = "P"
                self.ply = next_move
                time.sleep(0.25)
            if self.maze[next_move.y][next_move.x] == "E":
                self.printEND()
                return False
        return True

    def find_path(self):
        stack = [(self.ply.y, self.ply.x, [])]  # ใช้ stack แทน deque
        visited = set()
        
        while stack:
            y, x, path = stack.pop()  # ดึงข้อมูลจาก stack (DFS)
            if (y, x) in visited:
                continue
            visited.add((y, x))
            path = path + [(y, x)]

            # ถ้าเจอทางออก
            if (y, x) == (self.end.y, self.end.x):
                return path
            
            # ลำดับการเคลื่อนที่ (up, down, left, right)
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = y + dy, x + dx
                if self.isInBound(ny, nx) and self.maze[ny][nx] in [" ", "E"] and (ny, nx) not in visited:
                    stack.append((ny, nx, path))  # เพิ่มตำแหน่งใหม่ลงใน stack

        return None  # หากไม่พบเส้นทาง

    def auto_move(self):
        path = self.find_path()  # เรียกหาทางจาก DFS
        if path:
            for y, x in path:
                self.maze[self.ply.y][self.ply.x] = " "  # ลบผู้เล่นจากตำแหน่งเดิม
                self.ply = pos(y, x)
                self.maze[self.ply.y][self.ply.x] = "P"  # วางผู้เล่นในตำแหน่งใหม่
                self.print()
                time.sleep(0.5)  # พักเพื่อให้เห็นการเคลื่อนที่

class pos:
    def __init__(self, y, x) -> None:
        self.y = y
        self.x = x

if __name__ == '__main__':
    
    m = maze()
    m.print()
    m.auto_move()  # เริ่มการเดินทางสู่ความเวิ้งว้างอันไกลโพ้น
