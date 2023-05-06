import pygame


class Role():
    def __init__(self):
        # 加载飞船的图片,并对图片进行一定程度的缩放
        self.image = pygame.transform.scale(pygame.image.load('images/m.bmp'), (20, 20))
