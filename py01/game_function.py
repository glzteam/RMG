import sys
import pygame
import time


def draw_photo(data, screen, player_pos, player_image, image_width, image_height, image_data):
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if (i, j) == player_pos:
                screen.blit(player_image, (j * image_width, i * image_height))
            else:
                screen.blit(image_data[i][j], (j * image_width, i * image_height))
    pygame.display.flip()


def draw_picture(data, screen, image_data, player_image, image_width, image_height, player_pos):
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            screen.blit(image_data[i][j], (j * image_width, i * image_height))
    screen.blit(player_image, (player_pos[1] * image_width, player_pos[0] * image_height))
    pygame.display.flip()


def trans_m_to_p(data, image_data, image0, image1):
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if data[i][j] == 0:
                image_data[i][j] = image0
            elif data[i][j] == 1:
                image_data[i][j] = image1


def response_key(player_pos, data, screen, image_data, player_image, image_width, image_height):
    # 键盘发生事件，判断相应的输出状态
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_UP:
                up_press_time = pygame.time.get_ticks()
                running = True
                while running:
                    time.sleep(0.05)
                    if player_pos[0] > 0 and data[player_pos[0] - 1][player_pos[1]] == 0:
                        down_time = pygame.time.get_ticks()
                        if down_time - up_press_time > 150:
                            player_pos[0] -= 1
                        draw_picture(data, screen, image_data, player_image, image_width, image_height, player_pos)
                        for ent in pygame.event.get():
                            if ent.type == pygame.KEYUP:
                                if ent.key == pygame.K_UP:
                                    running = False
                                    break
                    else:
                        break
            elif event.key == pygame.K_DOWN:
                up_press_time = pygame.time.get_ticks()
                running = True
                while running:
                    time.sleep(0.05)
                    if player_pos[0] < data.shape[0] - 1 and data[player_pos[0] + 1][player_pos[1]] == 0:
                        down_time = pygame.time.get_ticks()
                        if down_time - up_press_time > 150:
                            player_pos[0] += 1
                        draw_picture(data, screen, image_data, player_image, image_width, image_height, player_pos)
                        for ent in pygame.event.get():
                            if ent.type == pygame.KEYUP:
                                if ent.key == pygame.K_DOWN:
                                    running = False
                                    break
                    else:
                        break
            elif event.key == pygame.K_LEFT:
                up_press_time = pygame.time.get_ticks()
                running = True
                while running:
                    time.sleep(0.05)
                    if player_pos[1] > 0 and data[player_pos[0]][player_pos[1] - 1] == 0:
                        down_time = pygame.time.get_ticks()
                        if down_time - up_press_time > 150:
                            player_pos[1] -= 1
                        draw_picture(data, screen, image_data, player_image, image_width, image_height, player_pos)
                        for ent in pygame.event.get():
                            if ent.type == pygame.KEYUP:
                                if ent.key == pygame.K_LEFT:
                                    running = False
                                    break
                    else:
                        break
            elif event.key == pygame.K_RIGHT:
                up_press_time = pygame.time.get_ticks()
                running = True
                while running:
                    time.sleep(0.05)
                    if player_pos[1] < data.shape[1] - 1 and data[player_pos[0]][player_pos[1] + 1] == 0:
                        down_time = pygame.time.get_ticks()
                        if down_time - up_press_time > 150:
                            player_pos[1] += 1
                        draw_picture(data, screen, image_data, player_image, image_width, image_height, player_pos)
                        for ent in pygame.event.get():
                            if ent.type == pygame.KEYUP:
                                if ent.key == pygame.K_RIGHT:
                                    running = False
                                    break
                    else:
                        break
