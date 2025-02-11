import turtle

# กำหนดค่าคงที่สำหรับเขาวงกต
OBSTACLE = 'O'
PART_OF_PATH = 'P'
TRIED = 'T'
DEAD_END = 'D'
EXIT = 'E'  # กำหนดตัวแทนทางออก

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

        # ตั้งค่าตำแหน่งเริ่มต้นของเต่า
        self.x_translate = -self.columns_in_maze / 2
        self.y_translate = self.rows_in_maze / 2

        # ตั้งค่า Turtle
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
        """ ทำให้สามารถเข้าถึงเมทริกซ์ของเขาวงกตผ่าน index ได้ """
        return self.maze_list[idx]

# -----------------------------------------------
# ฟังก์ชันสำหรับค้นหาเส้นทางโดยใช้ DFS
# -----------------------------------------------

def search_from(maze, start_row, start_column):
    """ ใช้อัลกอริธึม DFS เพื่อค้นหาเส้นทางออกจากเขาวงกต """
    
    # อัปเดตตำแหน่งปัจจุบัน
    maze.update_position(start_row, start_column)

    # 1. ชนสิ่งกีดขวาง ➝ หยุด
    if maze[start_row][start_column] == OBSTACLE:
        return False

    # 2. เคยสำรวจมาก่อนแล้ว ➝ หยุด
    if maze[start_row][start_column] in (TRIED, DEAD_END):
        return False

    # 3. พบจุดออกจากเขาวงกต ➝ สำเร็จ
    if maze.is_exit(start_row, start_column):
        maze.update_position(start_row, start_column, PART_OF_PATH)
        print("Congratulations! You win. 🎉")  # แสดงข้อความเมื่อถึงทางออก
        return True

    # ทำเครื่องหมายว่าเคยสำรวจแล้ว
    maze.update_position(start_row, start_column, TRIED)

    # ลองเดินไป 4 ทิศทาง (ขึ้น, ลง, ซ้าย, ขวา)
    found = (search_from(maze, start_row - 1, start_column) or
             search_from(maze, start_row + 1, start_column) or
             search_from(maze, start_row, start_column - 1) or
             search_from(maze, start_row, start_column + 1))

    # ถ้าพบเส้นทาง ➝ ทำเครื่องหมายเป็นเส้นทางที่ถูกต้อง
    if found:
        maze.update_position(start_row, start_column, PART_OF_PATH)
    else:
        maze.update_position(start_row, start_column, DEAD_END)

    return found

# -----------------------------------------------
# เรียกใช้งาน Maze และ ค้นหาเส้นทาง
# -----------------------------------------------
my_maze = Maze('Map1.txt')  # อ่านไฟล์เขาวงกต
my_maze.draw_maze()  # วาดเขาวงกต
my_maze.update_position(my_maze.start_row, my_maze.start_col)  # ตั้งค่าตำแหน่งเริ่มต้น

# ค้นหาเส้นทางออก
search_from(my_maze, my_maze.start_row, my_maze.start_col)

# หยุดการทำงานของ turtle
turtle.done()
