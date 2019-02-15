import os
import pygame
import random
from Life import Board


chanse = [2, 4, 8]


class Game_2048:
    def __init__(self, board_size, v=20):
        Board.__init__(self, board_size)
        self.game_over = False
        self.v = v
        self.clock = pygame.time.Clock()

    def set_viev(self, board_configs=(0, 0, 20)):
        pygame.init()
        Board.set_view(self, board_configs)
        self.screen = pygame.display.set_mode((
            self.board_size[0] * self.cell_size + self.left * 2,
            self.board_size[1] * self.cell_size + self.top * 2 +
            self.cell_size * 2))
        self.board = [[0] * self.board_size[0]
                      for _ in range(self.board_size[1])]
        fullname = os.path.join('data', 'gameover.jpg')
        image = pygame.image.load(fullname).convert()
        self.image_1 = pygame.transform.scale(image, (self.cell_size *
                                                      self.board_size[0],
                                                      self.cell_size *
                                                      (self.board_size[1] +
                                                       2)))

    def render(self):  # блок отрисовки картинки
        self.screen.fill((100, 100, 100))
        if self.game_over:  # конец игры
            self.screen.blit(self.image_1, self.image_1.get_rect())
            return None  # это чтобы больше ничего не отрисовывалось
        # рисовыние сетки и клеток с цифрами
        for y in range(self.board_size[1]):
            for x in range(self.board_size[0]):
                w = self.left + self.cell_size * x
                h = self.top + self.cell_size * y
                pygame.draw.rect(self.screen, (255, 255, 0),
                                 (w, h, self.cell_size, self.cell_size), 1)
                if self.board[y][x] != 0:  # сли клетка не пустая
                    # то написать цифру в кружочке
                    font = pygame.font.Font(None, self.cell_size)
                    text = font.render(
                        str(self.board[y][x]), 1, pygame.Color('red'))
                    pygame.draw.circle(self.screen, (0, 0, 255),
                                       (self.cell_size * x +
                                        self.cell_size // 2,
                                        self.cell_size * y +
                                        self.cell_size // 2),
                                       self.cell_size // 2 - 3)
                    self.screen.blit(
                        text, (self.cell_size * x + self.cell_size // 2 -
                               text.get_width() // 2, self.cell_size * y +
                               self.cell_size // 2 - text.get_height() // 2))
        # отрисовка нижнего ряда
        for i in range(self.board_size[0]):
            h = self.top + self.cell_size * (self.board_size[1] + 1)
            w = self.left + self.cell_size * i
            pygame.draw.rect(self.screen, (255, 50, 50),
                             (w, h, self.cell_size, self.cell_size), 1)
        # отрисовка ещё неезафиксированной клетки
        font = pygame.font.Font(None, self.cell_size)
        text = font.render(str(self.num), 1, pygame.Color('red'))
        pygame.draw.circle(self.screen, (0, 0, 255),
                           (self.num_cords[0],
                            round(self.num_cords[1])),
                           self.cell_size // 2 - 3)
        self.screen.blit(
            text, (self.num_cords[0] - text.get_width() // 2,
                   self.num_cords[1] - text.get_height() // 2))

    def start_game(self):  # сама игра
        self.num = random.choice(chanse)
        self.num_cords = [int(self.board_size[0] * self.cell_size // 2),
                          self.board_size[1] * self.cell_size +
                          self.cell_size // 2]
        self.dnum = None
        running = self.flag = True
        while running:  # оснвнй цикл
            for event in pygame.event.get():
                # релизуем управление
                if event.type == pygame.QUIT:  # выключение
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and self.flag:
                    self.flag = False
                    self.get_click(event.pos)
                    self.flag = True
                focus = self.get_cell(pygame.mouse.get_pos())
                if focus is not None and self.flag:
                    self.num_cords = [focus * self.cell_size +
                                      self.cell_size // 2,
                                      self.cell_size *
                                      (self.board_size[1] + 1) +
                                      self.cell_size // 2]
                elif focus is None and self.flag:
                    self.num_cords = [int(self.board_size[0] *
                                          self.cell_size // 2),
                                      self.board_size[1] * self.cell_size +
                                      self.cell_size // 2]
                if all([x != 0 for x in self.board[self.board_size[1] - 1]]):
                    self.game_over = True
                    self.flag = False
            self.render()
            pygame.display.flip()
        pygame.quit()

    def get_cell(self, mouse_pos):  # возвращает позицию мыши
        # по оси х числом от 0 до (ширины поля - 1)
        # если мышка находится в нижнем ряду
        h = self.top + self.cell_size * (self.board_size[1] + 1)
        for x in range(self.board_size[0]):
            w = self.left + self.cell_size * x
            if w + self.cell_size >= mouse_pos[0] > w and \
               h + self.cell_size >= mouse_pos[1] > h:
                return x
        return None  # иначе вернёт None

    def on_click(self, pos):  # поднимание нажатой улетки вверх
        y = 0
        for row in self.board:
            if row[pos] != 0:
                y += 1
        yd = self.cell_size * y + self.cell_size // 2
        run = True
        while run:
            self.render()  # отрисовка
            self.num_cords[1] -= self.v
            if self.num_cords[1] <= yd:
                self.num_cords[1] = yd
                self.board[y][pos] = self.num
                run = False
            pygame.display.flip()
            self.clock.tick(60)
        # и проверка на нличие
        # схожего (по числу) соседа
        self.check_board(pos, y)
        self.num = random.choice(chanse)
        self.num_cords = [int(self.board_size[0] * self.cell_size // 2),
                          self.board_size[1] * self.cell_size +
                          self.cell_size // 2]

    def get_click(self, pos):
        x = self.get_cell(pos)  # курсор в нижнем ряду?
        if x is not None:
            if self.board[self.board_size[1] - 1][x] == 0:
                self.on_click(x)  # тогда подними его

    def near(self, x, y):  # проверка на наличие схожего соседа
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dy * dx != 0:
                    continue
                if x + dx < 0 or x + dx >= self.board_size[0] or \
                   y + dy < 0 or y + dy >= self.board_size[1] or \
                   dx == dy == 0:
                    continue
                if self.board[y + dy][x + dx] == self.board[y][x]:
                    return x + dx, y + dy
        return None, None

    def check_board(self, x=None, y=None):  # проверка соседей и анимация
        dx, dy = self.near(x, y)
        # если есть сосед с таким же числом
        if dx is not None:
            self.board[y][x] = 0
            if x > dx:
                xconst = -1
            elif x < dx:
                xconst = 1
            else:
                xconst = None
            if y > dy:
                yconst = -1
            else:
                yconst = 1
            run = True
            while run:
                # обновление позиции незафиксированной клетки
                if xconst is not None:
                    self.num_cords[0] += self.v // 4 * xconst
                    if xconst < 0 and self.num_cords[0] <= \
                            dx * self.cell_size + self.cell_size // 2:
                        run = False
                        self.num_cords[0] = dx * \
                            self.cell_size + self.cell_size // 2
                    elif xconst > 0 and self.num_cords[0] >= \
                            dx * self.cell_size + self.cell_size // 2:
                        run = False
                        self.num_cords[0] = dx * \
                            self.cell_size + self.cell_size // 2
                else:
                    self.num_cords[1] += self.v // 4 * yconst
                    if yconst < 0 and self.num_cords[1] <= dy * \
                            self.cell_size + self.cell_size // 2:
                        run = False
                        self.num_cords[1] = dy * \
                            self.cell_size + self.cell_size // 2
                    elif yconst > 0 and self.num_cords[1] >= dy * \
                            self.cell_size + self.cell_size // 2:
                        run = False
                        self.num_cords[1] = dy * \
                            self.cell_size + self.cell_size // 2
                self.render()  # отрисовка на экран
                pygame.display.flip()  # бновить экран
                self.clock.tick(60)  # ну и задержка
            self.board[dy][dx] *= 2
            self.check_board(dx, dy)  # и снова проверка


if __name__ == '__main__':
    g = Game_2048((3, 3))  # для теста
    g.set_viev((0, 0, 50))
    g.start_game()
