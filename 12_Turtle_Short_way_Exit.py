from collections import deque
import turtle

# กำหนดค่าคงที่
OBSTACLE = 'O'
PART_OF_PATH = 'P'
TRIED = 'T'
DEAD_END = 'D'
EXIT = 'E'
START = 'S'

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
        """ วาดเขาวงกต """
        for y in range(self.rows_in_maze):
            for x in range(self.columns_in_maze):
                if self.maze_list[y][x] == OBSTACLE:
                    self.draw_centered_box(x + self.x_translate, -y + self.y_translate, 'tan')
                elif self.maze_list[y][x] == EXIT:
                    self.draw_centered_box(x + self.x_translate, -y + self.y_translate, 'yellow')
        self.t.color('black', 'blue')

    def draw_centered_box(self, x, y, color):
        """ วาดกล่องที่ตำแหน่ง x, y """
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
        """ วางร่องรอย """
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
        """ ตรวจสอบว่าตำแหน่งนี้คือทางออกหรือไม่ """
        return self.maze_list[row][col] == EXIT

    def __getitem__(self, idx):
        return self.maze_list[idx]


# -------------------------------------------------
# BFS หาเส้นทางที่สั้นที่สุด + ทิ้งร่องรอย
# -------------------------------------------------
def bfs_find_path(maze, start_row, start_col):
    """ ใช้ BFS หาเส้นทางไปยังทางออก พร้อมทิ้งร่องรอยการสำรวจ """
    queue = deque()
    queue.append((start_row, start_col))
    
    came_from = {}  # เก็บเส้นทางย้อนกลับ
    came_from[(start_row, start_col)] = None

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # ขึ้น ลง ซ้าย ขวา

    while queue:
        row, col = queue.popleft()

        #เจอทางออกแล้ว หยุดการค้นหา
        if maze.is_exit(row, col):
            return reconstruct_path(came_from, (start_row, start_col), (row, col))

        #วางร่องรอยว่าได้สำรวจจุดนี้แล้ว
        if (row, col) != (start_row-1, start_col):
            maze.update_position(row, col, TRIED)

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            if (0 <= new_row < maze.rows_in_maze and 0 <= new_col < maze.columns_in_maze and
                maze[new_row][new_col] not in (OBSTACLE, TRIED) and
                (new_row, new_col) not in came_from):

                queue.append((new_row, new_col))
                came_from[(new_row, new_col)] = (row, col)

    return None  # ถ้าไม่มีเส้นทาง


def reconstruct_path(came_from, start, end):
    """ สร้างเส้นทางย้อนกลับจากจุดสิ้นสุดไปจุดเริ่มต้น """
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()  # กลับลำดับเส้นทาง
    return path


# -------------------------------------------------
# ควบคุมการเดินของเต่า
# -------------------------------------------------
def move_turtle_along_path(maze, path):
    """ ให้เต่าเดินตามเส้นทางที่หาไว้ """
    for row, col in path:
        maze.update_position(row, col, PART_OF_PATH)


# -------------------------------------------------
# เรียกใช้งาน Maze และ ค้นหาเส้นทาง
# -------------------------------------------------
my_maze = Maze('Map1.txt')
my_maze.draw_maze()

#หาเส้นทางที่สั้นที่สุดไปยังทางออก พร้อมทิ้งร่องรอย
path_to_exit = bfs_find_path(my_maze, my_maze.start_row, my_maze.start_col)

if path_to_exit:
    print("พบเส้นทางไปทางออก!")

    #กลับไปจุดเริ่มต้น
    my_maze.update_position(my_maze.start_row, my_maze.start_col)

    #เดินไปยังทางออกตามเส้นทางที่หาไว้
    move_turtle_along_path(my_maze, path_to_exit)

else:
    print("ไม่พบเส้นทางไปทางออก")

turtle.done()
