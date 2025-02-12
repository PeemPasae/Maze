import os

class Maze:
    def __init__(self, maze_file_name):
        """ ตรวจสอบโฟลเดอร์และไฟล์ก่อนเปิดใช้งาน """
        maze_folder = "Maze"
        maze_path = os.path.join(maze_folder, maze_file_name)

        # ตรวจสอบว่าโฟลเดอร์มีอยู่หรือไม่
        if not os.path.isdir(maze_folder):
            raise FileNotFoundError(f"❌ ไม่พบโฟลเดอร์: {maze_folder}, กรุณาตรวจสอบเส้นทาง!")

        # ตรวจสอบว่าไฟล์มีอยู่หรือไม่
        if not os.path.isfile(maze_path):
            raise FileNotFoundError(f"❌ ไม่พบไฟล์: {maze_path}, กรุณาตรวจสอบชื่อไฟล์!")

        # อ่านไฟล์เขาวงกต
        self.maze_list = []
        self.start_row = None
        self.start_col = None

        with open(maze_path, 'r') as maze_file:
            for row_index, line in enumerate(maze_file):
                row_list = list(line.strip())
                if 'S' in row_list:
                    self.start_row = row_index
                    self.start_col = row_list.index('S')
                self.maze_list.append(row_list)

        self.rows_in_maze = len(self.maze_list)
        self.columns_in_maze = len(self.maze_list[0]) if self.maze_list else 0

        print("✅ โหลดเขาวงกตสำเร็จ!")

# ทดลองสร้างออบเจ็กต์ Maze
try:
    my_maze = Maze('Map1.txt')
except FileNotFoundError as e:
    print(e)
