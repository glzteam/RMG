import pygame
import time
import numpy as np
import ctypes, ctypes.util


class Game():

    """
    参数设定
    """
    def __init__(self, difficulty=1):

        # 加载角色和背景的图片,并对图片进行一定程度的缩放
        self.image = pygame.transform.scale(pygame.image.load('python_game/images/m.bmp'), (8, 8))
        self.imageEnd = pygame.transform.scale(pygame.image.load('python_game/images/end.bmp'), (8, 8))
        self.image0 = pygame.transform.scale(pygame.image.load('python_game/images/str1.bmp'), (8, 8))
        self.image1 = pygame.transform.scale(pygame.image.load('python_game/images/str2.bmp'), (8, 8))

        # 设置角色和终点位置
        self.player_pos = [4, 6]
        self.end_pos = [95, 190]

        # 游戏限时
        self.game_time_limit = 30

        self.flag = False

        # 判断程序结束的标识
        self.identification = 0

        # 当前游戏难度
        self.difficulty = difficulty

        # 调用C++函数生成地图时的地图控制参数
        self.length = 100  # 地图的长度
        self.width = 200  # 地图的宽度
        self.room_R_ = 5  # 房间半径上限
        self.room_r_ = 3  # 房间半径下限
        self.room_num_ = 30  # 房间数量
        self.room_edge_ = 8  # 与地图边缘的最小距离
        self.room_min_dis_ = 15  # 房间之间最小距离（圆心）
        self.path_r_ = 1  # 路径半宽度
        self.path_step_ = 3  # 路径生成步长
        self.max_path_len_ = 100000000000000000  # 最长路径长度
        self.ring_path_num_ = 0  # 生成树完成之后增加的路径数量

    """
    out_matrix调用C++地图生成函数，产生地图参数
    """

    def out_matrix(self):
        try:
            dll_path = ctypes.util.find_library("./RandProject.dll")
            # 加载动态库，若失败则抛出异常
            vc_dll = ctypes.CDLL(dll_path)
            # 获取动态库的函数
            vc_func = vc_dll.generate

            # 设置一个二维指针，指向生成过程中产生的二维矩阵
            num = 1010
            mp_array = ctypes.c_int * num * num
            mp = mp_array()

            # 地图房间的数量
            room_num_ = self.room_num_ + 15 * self.difficulty

            # 做类型适配
            vc_func.argtypes = [
                ctypes.POINTER(mp_array),
                ctypes.c_int,
                ctypes.c_int,
                ctypes.c_int,
                ctypes.c_int,
                ctypes.c_int,
                ctypes.c_int,
                ctypes.c_double,
                ctypes.c_double,
                ctypes.c_double,
                ctypes.c_int,
                ctypes.c_int
            ]

            # 该处是调用C++的函数，设置欲传递的参数，传入后得到预期的结果
            vc_func(ctypes.byref(mp),
                    self.length,
                    self.width,
                    self.room_R_,
                    self.room_r_,
                    room_num_,
                    self.room_edge_,
                    self.room_min_dis_,
                    self.path_r_,
                    self.path_step_,
                    self.max_path_len_,
                    self.ring_path_num_)

            # 将二维矩阵转换为 Python 中的列表
            matrix = [[mp[i][j] for j in range(self.width)] for i in range(self.length)]
            return matrix
        except OSError as e:
            print(e, "加载dll失败")

    """
    绘制游戏过程中完整的游戏界面
    """
    def draw_photo(self, data, screen, player_pos, end_pos, player_image, end_image, image_width, image_height, image_data):
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                if (i, j) == player_pos:
                    screen.blit(player_image, (j * image_width, i * image_height))
                elif (i, j) == end_pos:
                    screen.blit(end_image, (j * image_width, i * image_height))
                else:
                    screen.blit(image_data[i][j], (j * image_width, i * image_height))
        pygame.display.flip()

    """
    绘制每次按键事件触发后的游戏界面
    """
    def draw_picture(self, data, screen, image_data, player_image, end_image, image_width, image_height, player_pos, end_pos):
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                screen.blit(image_data[i][j], (j * image_width, i * image_height))
        screen.blit(player_image, (player_pos[1] * image_width, player_pos[0] * image_height))
        screen.blit(end_image, (end_pos[1] * image_width, end_pos[0] * image_height))

    """
    在0和1组成的矩阵表面粘贴图片，生成游戏背景
    """
    def trans_m_to_p(self, data, image_data, image0, image1):
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                if data[i][j] == 0:
                    image_data[i][j] = image0
                elif data[i][j] == 1:
                    image_data[i][j] = image1

    """
    moving_up  moving_down  moving_left  moving_right检测角色的移动
    """
    def moving_up(self, player_pos, data):
        if player_pos[0] > 0 and data[player_pos[0] - 1][player_pos[1]] == 0:
            player_pos[0] -= 1

    def moving_down(self, player_pos, data):
        if player_pos[0] < data.shape[0] - 1 and data[player_pos[0] + 1][player_pos[1]] == 0:
            player_pos[0] += 1

    def moving_left(self, player_pos, data):
        if player_pos[1] > 0 and data[player_pos[0]][player_pos[1] - 1] == 0:
            player_pos[1] -= 1

    def moving_right(self, player_pos, data):
        if player_pos[1] < data.shape[1] - 1 and data[player_pos[0]][player_pos[1] + 1] == 0:
            player_pos[1] += 1

    """
    游戏前的准备阶段，直到生成最初的静止游戏界面
    """
    def run_game(self):
        # 初始化Pygame
        pygame.init()

        # 设置游戏窗口图标和名称
        pygame.display.set_caption(" iKun 打篮球")
        icon = pygame.image.load('python_game/images/icon.png')
        pygame.display.set_icon(icon)

        self.font = pygame.font.Font(None, 36)

        self.start_time = time.time()

        # 生成二维矩阵，并将其赋值给dataX
        self.data = np.array(self.out_matrix())
        # 参数设置
        self.image_width = self.image0.get_width()
        self.image_height = self.image0.get_height()
        screen_width = self.image_width * self.data.shape[1]
        screen_height = self.image_height * self.data.shape[0]

        # 将二维矩阵转换为图像表面对象
        self.image_data = np.empty((self.data.shape[0], self.data.shape[1]), dtype=pygame.Surface)
        self.trans_m_to_p(self.data, self.image_data, self.image0, self.image1)

        # 生成一定大小的游戏运行窗
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        # 生成最初的游戏画面
        self.draw_photo(self.data, self.screen, self.player_pos, self.end_pos, self.image, self.imageEnd, self.image_width, self.image_height, self.image_data)
        # 设置按键重复
        pygame.key.set_repeat(pygame.KEYDOWN, 1000)

    """
    判决角色的移动，角色移动模块
    """
    def check_game_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.identification = 1
                pygame.quit()

        # 获取当前按下的按键
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.identification = 1
            pygame.quit()

        # 根据按键状态移动对象
        if keys[pygame.K_UP]:
            self.moving_up(self.player_pos, self.data)
        if keys[pygame.K_DOWN]:
            self.moving_down(self.player_pos, self.data)
        if keys[pygame.K_LEFT]:
            self.moving_left(self.player_pos, self.data)
        if keys[pygame.K_RIGHT]:
            self.moving_right(self.player_pos, self.data)
        time.sleep(0.01)
        # 绘制图像
        self.draw_picture(self.data, self.screen, self.image_data, self.image, self.imageEnd, self.image_width, self.image_height, self.player_pos, self.end_pos)

    """
    判决游戏退出的函数，计时模块
    """
    def check_game_time(self):
        present_time = time.time() - self.start_time
        remain_time = self.game_time_limit - present_time

        if remain_time <= 0:
            self.identification = 3
            pygame.quit()

        time_str = "Time:{}s".format(int(remain_time))
        text = self.font.render(time_str, True, (255, 255, 255))
        self.screen.blit(text, (1480, 20))
        pygame.display.flip()

    """
    判断游戏角色是否到达了终点
    """
    def check_end(self):
        if self.player_pos == [95, 190]:
            self.identification = 2
            pygame.quit()


if __name__ == '__main__':
    game = Game(1)
    game.run_game()
    while True:
        game.check_game_time()
        game.check_game_keys()
        game.check_end()
