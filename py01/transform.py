import pygame
import numpy as np
import game_function as gf
from role import Role
from getMatrix import out_matrix

# 初始化Pygame
pygame.init()

# 加载图片
image0 = pygame.transform.scale(pygame.image.load('images/str1.bmp'), (20, 20))
image1 = pygame.transform.scale(pygame.image.load('images/str2.bmp'), (20, 20))

# 实例化对象
role = Role()
# 创建时钟对象
clock = pygame.time.Clock()
# 计算每帧的时间间隔
dt = clock.tick(60) / 1000.0  # 60帧每秒
speed = 100  # 每秒100个像素
distance = speed * dt  # 根据时间计算应该移动的距离

# 设置长按阈值为 500 毫秒
LONG_PRESS_THRESHOLD = 500

# 用于记录 W 键的按下时间
w_down_time = 0

# if duration >= LONG_PRESS_THRESHOLD:
#     print("空格键被长按了！")
# else:
#     print("空格键被按了一次！")

# 生成二维矩阵，并将其赋值给data
data = np.array(out_matrix())

# 将二维矩阵转换为图像表面对象
image_data = np.empty((data.shape[0], data.shape[1]), dtype=pygame.Surface)
gf.trans_m_to_p(data, image_data, image0, image1)

# 设置角色初始位置
player_pos = [0, 0]

# 参数设置
image_width = image0.get_width()
image_height = image0.get_height()
screen_width = image_width * data.shape[1]
screen_height = image_height * data.shape[0]
screen = pygame.display.set_mode((screen_width, screen_height))
# 生成最初的游戏画面
gf.draw_photo(data, screen, player_pos, role.image, image_width, image_height, image_data)

# 事件循环
while True:
    # 检测键盘事件，根据接收的事件角色做出相应的响应
    gf.response_key(player_pos, data, screen, image_data, role.image, image_width, image_height)
    # 绘制图像
    gf.draw_picture(data, screen, image_data, role.image, image_width, image_height, player_pos)
