import turtle
from collections import deque
import time

# กำหนดค่าคงที่
OBSTACLE = 'X'
PART_OF_PATH = 'P'
TRIED = 'T'
EXIT = 'E'
START = 'S'
EMPTY = ' '

class MazeData:
    """ คลาสสำหรับเก็บข้อมูลเขาวงกต """
    def __init__(self):
        self.maze = [
            ["X", "X", "X", "X", "X", "X", "X"],
            ["X", "S", " ", " ", "X", " ", "X"],
            ["X", " ", "X", " ", "X", " ", "E"],
            ["X", " ", "X", " ", "X", " ", "X"],
            ["X", " ", "X", " ", " ", " ", "X"],
            ["X", " ", "X", "X", "X", "X", "X"],
        ]
    
    def get_maze(self):
        """ คืนค่าเมทริกซ์ของเขาวงกต """
        return self.maze

class Maze:
    def __init__(self, draw_speed=10):
        """ โหลดเขาวงกตจาก MazeData """
        maze_data = MazeData()
        self.maze_list = maze_data.get_maze()
        self.start_position = None
        self.exit_position = None

        for row_index, row in enumerate(self.maze_list):
            for col_index, cell in enumerate(row):
                if cell == START:
                    self.start_position = (row_index, col_index)
                elif cell == EXIT:
                    self.exit_position = (row_index, col_index)

        self.rows = len(self.maze_list)
        self.cols = len(self.maze_list[0])

        # ตั้งค่า Turtle
        self.t = turtle.Turtle(shape='turtle')
        self.t.speed(draw_speed)  # ปรับความเร็วการวาดแผนที่ตามที่กำหนด
        turtle.setup(width=600, height=600)
        turtle.setworldcoordinates(-0.5, -self.rows + 0.5, self.cols - 0.5, 0.5)

        self.t.up()

    def draw_maze(self, fast=False):
        """ ให้เต่าเป็นคนวาดแผนที่ """
        for y in range(self.rows):
            for x in range(self.cols):
                if self.maze_list[y][x] == OBSTACLE:
                    self.draw_box(x, -y, 'tan')
                elif self.maze_list[y][x] == EXIT:
                    self.draw_box(x, -y, 'yellow')
                elif self.maze_list[y][x] == START:
                    self.draw_box(x, -y, 'blue')

                if fast:
                    time.sleep(0.01)  # เพิ่มเวลาหน่วงระหว่างการวาดแผนที่เพื่อให้ดูชัดเจน

    def draw_box(self, x, y, color):
        """ เต่าวาดกล่องสี่เหลี่ยมที่ตำแหน่ง x, y """
        self.t.up()
        self.t.goto(x, y)
        self.t.down()
        self.t.color('black', color)
        self.t.begin_fill()
        for _ in range(4):
            self.t.forward(1)
            self.t.right(90)
        self.t.end_fill()

    def move_turtle(self, row, col):
        """ เคลื่อนที่เต่าไปยังตำแหน่ง row, col """
        self.t.up()
        self.t.goto(col, -row)
        self.t.down()

    def drop_bread_crumb(self, color):
        """ วางร่องรอยที่ตำแหน่งปัจจุบัน """
        self.t.dot(10, color)

    def update_position(self, row, col, val=None):
        """ อัปเดตตำแหน่งในเมทริกซ์และให้เต่าเดินไป """
        if val:
            self.maze_list[row][col] = val
        self.move_turtle(row, col)

        color_mapping = {
            PART_OF_PATH: 'green',
            OBSTACLE: 'red',
            TRIED: 'gray'
        }
        color = color_mapping.get(val, None)
        if color:
            self.drop_bread_crumb(color)

    def is_exit(self, row, col):
        """ เช็คว่าตำแหน่งปัจจุบันเป็นทางออกหรือไม่ """
        return self.maze_list[row][col] == EXIT

    def __getitem__(self, idx):
        """ ทำให้สามารถเข้าถึงเมทริกซ์ของเขาวงกตผ่าน index ได้ """
        return self.maze_list[idx]

    def display_success_message(self):
        """ พิมพ์ข้อความยินดีเมื่อพบทางออก """
        self.t.up()
        self.t.goto(0, 0)  # ตั้งตำแหน่งที่เต่าจะเริ่มพิมพ์
        self.t.color('green')
        self.t.write("ยินดี! คุณหาทางออกได้แล้ว! 🎉", align="center", font=("Arial", 16, "bold"))

# -----------------------------------------------
# ฟังก์ชันสำหรับค้นหาเส้นทางโดยใช้ BFS
# -----------------------------------------------

def bfs_search(maze):
    """ ใช้อัลกอริธึม BFS เพื่อค้นหาเส้นทางออกจากเขาวงกต """
    queue = deque()
    visited = set()
    predecessors = {}

    start_row, start_col = maze.start_position  # ใช้ตำแหน่งที่เป็น "S"
    queue.append((start_row, start_col))
    visited.add((start_row, start_col))
    maze.update_position(start_row, start_col, TRIED)

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # ขึ้น, ลง, ซ้าย, ขวา

    while queue:
        row, col = queue.popleft()

        if maze.is_exit(row, col):
            print("🎉 พบเส้นทางออก! กำลังวาดเส้นทางที่สั้นที่สุด...")
            reconstruct_path(maze, predecessors, row, col)
            maze.display_success_message()  # แสดงข้อความยินดี
            return True

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            if (0 <= new_row < maze.rows and 0 <= new_col < maze.cols and
                    (new_row, new_col) not in visited and maze[new_row][new_col] != OBSTACLE):

                queue.append((new_row, new_col))
                visited.add((new_row, new_col))
                predecessors[(new_row, new_col)] = (row, col)  # บันทึกเส้นทางย้อนกลับ
                maze.update_position(new_row, new_col, TRIED)
                time.sleep(0.05)  # หน่วงเวลาให้เดินเห็นชัดขึ้น

    print("🚫 ไม่พบเส้นทางออก!")
    return False

def reconstruct_path(maze, predecessors, row, col):
    """ วาดเส้นทางที่สั้นที่สุดโดยย้อนจากจุดออกไปยังจุดเริ่มต้น """
    path = []
    while (row, col) in predecessors:
        path.append((row, col))
        row, col = predecessors[(row, col)]

    path.reverse()  # ให้เดินจากต้นทางไปปลายทาง

    for row, col in path:
        maze.update_position(row, col, PART_OF_PATH)
        time.sleep(0.05)  # ให้เดินแบบเห็นการเคลื่อนที่ชัดขึ้น

# -----------------------------------------------
# เรียกใช้งาน Maze และ ค้นหาเส้นทาง
# -----------------------------------------------

def main():
    my_maze = Maze(draw_speed=5)  # ปรับความเร็วการวาดแผนที่

    # วาดแผนที่และตรวจหาทางออกพร้อมกัน
    found_exit = False
    for y in range(my_maze.rows):
        for x in range(my_maze.cols):
            if my_maze.maze_list[y][x] == EXIT:
                found_exit = True
                break
        if found_exit:
            break

    if not found_exit:
        print("🚶‍♂️ ไม่พบทางออกที่แผนที่, เต่าจะทำการสำรวจ...")
        my_maze.draw_maze(fast=True)  # วาดแผนที่และเดินสำรวจแบบเร็ว
    else:
        print("🧐 พบทางออก, เริ่มค้นหาเส้นทางไปทางออกทันที!")
        my_maze.draw_maze(fast=False)  # วาดแผนที่ในโหมดช้า
        bfs_search(my_maze)  # ค้นหาเส้นทางออกโดยใช้ BFS

    turtle.done()

if __name__ == "__main__":
    main()
