import pygame


class IMAGE():
    def __init__(self, data):
        self.image0 = pygame.transform.scale(pygame.image.load('images/str1.bmp'), (20, 20))
        self.image1 = pygame.transform.scale(pygame.image.load('images/str2.bmp'), (20, 20))

        # 参数设置
        self.image_width = self.image0.get_width()
        self.image_height = self.image0.get_height()
        self.screen_width = self.image_width * data.shape[1]
        self.screen_height = self.image_height * data.shape[0]