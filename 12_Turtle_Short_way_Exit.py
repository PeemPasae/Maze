import turtle
from collections import deque

# กำหนดค่าคงที่สำหรับเขาวงกต
OBSTACLE = 'O'
PART_OF_PATH = 'P'
TRIED = 'T'
DEAD_END = 'D'
EXIT = 'E'

class Maze:
    def __init__(self, maze_file_name):
        """ อ่านไฟล์และสร้างเมทริกซ์สำหรับเขาวงกต """
        self.maze_list = []
        self.start_row = None
        self.start_col = None

        with open(f'Maze/{maze_file_name}', 'r') as maze_file:
            for row_index, line in enumerate(maze_file):
                row_list = list(line.strip())
                if 'S' in row_list:
                    self.start_row = row_index
                    self.start_col = row_list.index('S')
                self.maze_list.append(row_list)

        self.rows_in_maze = len(self.maze_list)
        self.columns_in_maze = len(self.maze_list[0]) if self.maze_list else 0

        self.x_translate = -self.columns_in_maze / 2
        self.y_translate = self.rows_in_maze / 2

        self.t = turtle.Turtle(shape='turtle')
        turtle.setup(width=600, height=600)
        turtle.setworldcoordinates(- (self.columns_in_maze - 1) / 2 - 0.5,
                                   - (self.rows_in_maze - 1) / 2 - 0.5,
                                   (self.columns_in_maze - 1) / 2 + 0.5,
                                   (self.rows_in_maze - 1) / 2 + 0.5)

    def draw_maze(self):
        """ วาดเขาวงกตโดยใช้ turtle """
        for y in range(self.rows_in_maze):
            for x in range(self.columns_in_maze):
                if self.maze_list[y][x] == OBSTACLE:
                    self.draw_centered_box(x + self.x_translate, -y + self.y_translate, 'tan')
                elif self.maze_list[y][x] == EXIT:
                    self.draw_centered_box(x + self.x_translate, -y + self.y_translate, 'yellow')
        self.t.color('black', 'blue')

    def draw_centered_box(self, x, y, color):
        """ วาดกล่องสี่เหลี่ยมที่ตำแหน่ง x, y """
        turtle.tracer(0)
        self.t.up()
        self.t.goto(x - 0.5, y - 0.5)
        self.t.color('black', color)
        self.t.setheading(90)
        self.t.down()
        self.t.begin_fill()
        for _ in range(4):
            self.t.forward(1)
            self.t.right(90)
        self.t.end_fill()
        turtle.update()
        turtle.tracer(1)

    def move_turtle(self, x, y):
        """ เคลื่อนที่เต่าไปยังตำแหน่ง x, y """
        self.t.up()
        self.t.setheading(self.t.towards(x + self.x_translate, -y + self.y_translate))
        self.t.goto(x + self.x_translate, -y + self.y_translate)

    def drop_bread_crumb(self, color):
        """ วางร่องรอยที่ตำแหน่งปัจจุบัน """
        self.t.dot(color)

    def update_position(self, row, col, val=None):
        """ อัปเดตตำแหน่งในเมทริกซ์และแสดงผล """
        if val:
            self.maze_list[row][col] = val
        self.move_turtle(col, row)

        color_mapping = {
            PART_OF_PATH: 'green',
            OBSTACLE: 'red',
            TRIED: 'black',
            DEAD_END: 'red'
        }
        color = color_mapping.get(val, None)
        if color:
            self.drop_bread_crumb(color)

    def is_exit(self, row, col):
        """ เช็คว่าตำแหน่งปัจจุบันเป็นทางออกหรือไม่ """
        return self.maze_list[row][col] == EXIT

    def __getitem__(self, idx):
        return self.maze_list[idx]

def bfs_find_path(maze, start_row, start_col):
    """ ใช้ BFS หาเส้นทางไปยังทางออก พร้อมทิ้งร่องรอยการสำรวจ """
    queue = deque()
    queue.append((start_row-1, start_col))

    came_from = {}
    came_from[(start_row, start_col)] = None

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # ขึ้น ลง ซ้าย ขวา

    # วางร่องรอยจุดเริ่มต้น
    maze.update_position(start_row, start_col, TRIED)

    while queue:
        row, col = queue.popleft()

        # เจอทางออกแล้ว หยุดการค้นหา
        if maze.is_exit(row, col):
            return reconstruct_path(came_from, (start_row, start_col), (row, col))

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            if (0 <= new_row < maze.rows_in_maze and 0 <= new_col < maze.columns_in_maze and
                maze[new_row][new_col] not in (OBSTACLE, TRIED) and
                (new_row, new_col) not in came_from):

                queue.append((new_row, new_col))
                came_from[(new_row, new_col)] = (row, col)

                # วางร่องรอยว่าได้สำรวจจุดนี้แล้ว
                maze.update_position(new_row, new_col, TRIED)

    return None  # ถ้าไม่มีเส้นทาง

def reconstruct_path(came_from, start, end):
    """ สร้างเส้นทางจากจุดเริ่มต้นไปยังทางออก """
    path = []
    current = end
    while current:
        path.append(current)
        current = came_from[current]

    path.reverse()  # ทำให้เส้นทางเรียงจากต้นทางไปปลายทาง
    return path

def follow_path(maze, path):
    """ ให้เต่าเดินตามเส้นทางที่หาได้ """
    for row, col in path:
        maze.update_position(row, col, PART_OF_PATH)

# ------------------------------------------------
# เรียกใช้งาน Maze และ ค้นหาเส้นทาง
# ------------------------------------------------
my_maze = Maze('Map1.txt')
my_maze.draw_maze()

#สแกนแผนที่เพื่อหาเส้นทางออก
path = bfs_find_path(my_maze, my_maze.start_row, my_maze.start_col)

if path:
    # กลับไปที่จุดเริ่มต้น
    my_maze.update_position(my_maze.start_row, my_maze.start_col)

    # เดินไปหาทางออกผ่านเส้นทางที่ดีที่สุด
    follow_path(my_maze, path)
    print("เดินออกสำเร็จ!")
else:
    print("ไม่พบเส้นทางออก")

turtle.done()