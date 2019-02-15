import os
import pygame
from random import choice


chanse = [0] * 8 + [1] * 2  # вероятность появления (2/10)


class Board:  # класс поля
    def __init__(self, board_size):
        self.board_size = list(board_size)
        self.board = [[0] * board_size[0]
                      for _ in range(board_size[1])]  # само поле
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, board_configs):
        self.left = board_configs[0]
        self.top = board_configs[1]
        self.cell_size = board_configs[2]

    def render(self):
        for y in range(self.board_size[1]):
            for x in range(self.board_size[0]):
                w = self.left + self.cell_size * x
                h = self.top + self.cell_size * y
                if self.setka:
                    pygame.draw.rect(self.screen, (100, 100, 100),
                                     (w, h, self.cell_size, self.cell_size), 1)
                if self.krug:
                    if self.board[y][x]:
                        pygame.draw.circle(self.screen, pygame.Color('green'),
                                           (w + self.cell_size // 2, h +
                                            self.cell_size // 2),
                                           self.cell_size // 2 - 2)
                else:
                    if self.board[y][x]:
                        pygame.draw.rect(self.screen, pygame.Color('green'),
                                         (w, h, self.cell_size,
                                          self.cell_size))

    def get_cell(self, mouse_pos):
        for y in range(self.board_size[1]):
            for x in range(self.board_size[0]):
                w = self.left + self.cell_size * x
                h = self.top + self.cell_size * y
                if w + self.cell_size >= mouse_pos[0] > w and \
                   h + self.cell_size >= mouse_pos[1] > h:
                    return x, y
        return None

    def on_click(self, cell_coords):
        i = 1
        if self.board[cell_coords[1]][cell_coords[0]]:
            i = 0
        self.board[cell_coords[1]][cell_coords[0]] = i

    def get_click(self, mouse_pos):
        cell_coords = self.get_cell(mouse_pos)
        if cell_coords is not None:
            self.on_click(cell_coords)

    def __str__(self):
        return self.board


class Life(Board):
    def __init__(self, board_size, v=20):
        Board.__init__(self, board_size)
        self.setka = self.krug = True
        self.v = v
        self.stop = True
        self.clock = pygame.time.Clock()
        self.bg = True

    def set_viev(self, board_configs=(0, 0, 20)):
        Board.set_view(self, board_configs)
        self.screen = pygame.display.set_mode((
            self.board_size[0] * self.cell_size + self.left * 2,
            self.board_size[1] * self.cell_size + self.top * 2))
        self.board = [[0] * self.board_size[0]
                      for _ in range(self.board_size[1])]
        # импорт заднего фона
        fullname = os.path.join('data', 'stars_bg.jpg')
        image = pygame.image.load(fullname).convert()
        self.bg = pygame.transform.scale(image, (self.cell_size *
                                                      self.board_size[0],
                                                      self.cell_size *
                                                      (self.board_size[1])))

    def start_life(self):  # начало жизни
        pygame.init()
        running = True
        while running:
            self.screen.fill((50, 50, 50))
            if self.bg:  # отрисовка заднего фона
                self.screen.blit(self.bg, self.bg.get_rect())
            for event in pygame.event.get():
                flag = True
                # релизуем управление
                if event.type == pygame.QUIT:  # выключение
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # нажтие на ЛКМ
                        self.get_click(event.pos)
                    if event.button == 2:  # нажатие на СКМ
                        self.v = 10  # скорость равна 10
                    if event.button == 3:  # нажатие на ПКМ
                        self.stop = False  # запуск "жизни"
                    if event.button == 4:  # прокрутка колёсика мыши вверх
                        self.v += 1   # увеличение скорости
                    if event.button == 5:  # прокрутка колёсика мыши вниз
                        if self.v > 1:
                            self.v -= 1  # уменьшение скорости
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # выключение
                        running = False
                    if event.key == pygame.K_r:  # нажатие клавиши "R"
                        # очистка поля
                        self.board = [
                            [0] * self.board_size[0]
                            for _ in range(self.board_size[1])]
                    if event.key == pygame.K_b:  # нажатие клавиши "B"
                        # включить/выключить задний фон
                        if self.bg:
                            self.bg = False
                        else:
                            self.bg = True
                    if event.key == pygame.K_t:  # нажатие клавиши "T"
                        # поставить живые клетки случайным образом
                        self.randomize()
                    if event.key == pygame.K_w:  # нажатие клавиши "W"
                        self.full_all()  # заставить поле полностью
                    if event.key == pygame.K_s:  # нажатие клавиши "S"
                        if self.setka:  # включить или отключить сетку
                            self.setka = False
                        else:
                            self.setka = True
                        flag = False
                    if event.key == pygame.K_q:  # нажатие клавиши "Q"
                        # выбор клетки в форме квадрата или же круга
                        if self.krug:
                            self.krug = False
                        else:
                            self.krug = True
                        flag = False
                    if event.key == pygame.K_UP:  # нажатие стрелки вверх
                        if self.board_size[1] > 3:
                            self.board_size[1] -= 1
                            self.set_viev((self.left, self.top,
                                           self.cell_size))
                    if event.key == pygame.K_DOWN:  # нажатие стрелки вниз
                        self.board_size[1] += 1
                        self.set_viev((self.left, self.top, self.cell_size))
                    if event.key == pygame.K_RIGHT:  # нажатие стрелки вправо
                        self.board_size[0] += 1
                        self.set_viev((self.left, self.top, self.cell_size))
                    if event.key == pygame.K_LEFT:  # нажатие стрелки влево
                        if self.board_size[0] > 3:
                            self.board_size[0] -= 1
                            self.set_viev((self.left, self.top,
                                           self.cell_size))
                    if event.key == pygame.K_EQUALS:  # нажатие клавиши "="
                        self.cell_size += 1
                        self.set_viev((self.left, self.top, self.cell_size))
                    if event.key == pygame.K_MINUS:  # нажатие клавиши "-"
                        if self.cell_size > 5:
                            self.cell_size -= 1
                            self.set_viev((self.left, self.top,
                                           self.cell_size))
                    if event.key == pygame.K_m:  # нажатие клавиши "M"
                        self.v = 0
                        flag = False
                    if event.key == pygame.K_SPACE:  # нажатие клавиши "Space"
                        if self.stop:  # запуск и остановка "жизни"
                            self.stop = False
                        else:
                            self.stop = True
                    elif not self.stop and flag:
                        self.stop = True
            self.render()
            if not self.stop:
                self.living()
                self.clock.tick(self.v)
            '''if pygame.mouse.get_focused() and self.stop:
                pos = pygame.mouse.get_pos()
                pygame.draw.circle(self.screen, pygame.Color('red'),
                                   (pos[0], pos[1]), 5)'''
            pygame.display.flip()
        pygame.quit()

    def on_click(self, cell_coords):
        if self.stop:
            Board.on_click(self, cell_coords)

    def living(self):
        boardI = []
        for y in range(self.board_size[1]):
            boardI.append(self.board[y][:])
        for y in range(self.board_size[1]):
            for x in range(self.board_size[0]):
                klet = self.near((x, y))
                if self.board[y][x] == 1 and not (klet == 3 or klet == 2):
                    boardI[y][x] = 0
                elif self.board[y][x] == 0 and klet == 3:
                    boardI[y][x] = 1
        self.board = boardI

    def randomize(self):
        for y in range(self.board_size[1]):
            for x in range(self.board_size[0]):
                self.board[y][x] = choice(chanse)

    def full_all(self):
        for y in range(self.board_size[1]):
            for x in range(self.board_size[0]):
                self.board[y][x] = 1

    def near(self, cell_coords):
        klet = 0
        a = [cell_coords[1] - 1, cell_coords[1], cell_coords[1] + 1]
        if cell_coords[1] == 0:
            a = [self.board_size[1] - 1, 0, 1]
        elif cell_coords[1] == self.board_size[1] - 1:
            a = [self.board_size[1] - 2, self.board_size[1] - 1, 0]
        for y in a:
            b = [cell_coords[0] - 1,
                 cell_coords[0], cell_coords[0] + 1]
            if cell_coords[0] == 0:
                b = [self.board_size[0] - 1, 0, 1]
            elif cell_coords[0] == self.board_size[0] - 1:
                b = [self.board_size[0] - 2, self.board_size[0] - 1, 0]
            for x in b:
                if self.board[y][x] == 1 and not (cell_coords[0] == x and
                                                  cell_coords[1] == y):
                    klet += 1
        return klet


# тест игры
if __name__ == '__main__':
    v = 20  # первоначальная скорость
    board_size = (20, 20)  # размер поля
    board_configs = (0, 0, 30)  # отступ слева (и справа),
    # отступ сверху (и снизу), размер клетки
    l = Life(board_size, v)
    l.set_viev(board_configs)
    l.start_life()
