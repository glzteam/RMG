import pygame
import numpy as np
import game_function as gf
from role import Role
from back_image import IMAGE
from settings import Settings

# 初始化Pygame
pygame.init()

# 实例化游戏设置，便于得到其中的参数，调用其中的函数
settings = Settings()

# 生成二维矩阵，并将其赋值给data
data = np.array(settings.out_matrix())

# 实例化对象
role = Role()
image = IMAGE(data)

# 将二维矩阵转换为图像表面对象
image_data = np.empty((data.shape[0], data.shape[1]), dtype=pygame.Surface)
gf.trans_m_to_p(data, image_data, image.image0, image.image1)

# 生成一定大小的游戏运行窗
screen = pygame.display.set_mode((image.screen_width, image.screen_height))
# 生成最初的游戏画面
gf.draw_photo(data, screen, role.player_pos, role.image, image.image_width, image.image_height, image_data)

# 事件循环
while True:
    # 检测键盘事件，根据接收的事件角色做出相应的响应
    gf.response_key(role.player_pos, data, screen, image_data, role.image, image.image_width, image.image_height)
    # 绘制图像
    gf.draw_picture(data, screen, image_data, role.image, image.image_width, image.image_height, role.player_pos)
