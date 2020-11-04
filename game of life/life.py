import pygame
from pygame.locals import *
import random
from pprint import pprint as pp


class GameOfLife:
    def __init__(self, width: int = 640,
                 height: int = 480,
                 cell_size: int = 80,
                 speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.clist = self.cell_list()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            # Отрисовка списка клеток
            self.draw_grid()
            self.draw_cell_list(self.clist)

            # Выполнение одного шага игры (обновление состояния ячеек)
            self.update_cell_list(self.clist)

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize: bool = True) -> list:
        """ Создание списка клеток.
        :param randomize: Если True, то создается список клеток, где
        каждая клетка равновероятно может быть живой (1) или мертвой (0).
        :return: Список клеток, представленный в виде матрицы
        """
        clist = []
        if randomize:
            for y in range(self.cell_height):
                clist.append([random.randint(0, 1) for x in range(self.cell_width)])
        else:
            for y in range(self.cell_height):
                clist.append([0 for x in range(self.cell_width)])
        return clist

    def draw_cell_list(self, clist: list) -> None:
        """ Отображение списка клеток
        :param rects: Список клеток для отрисовки, представленный в виде матрицы """
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                rect = (x * self.cell_size + 1,
                        y * self.cell_size + 1,
                        self.cell_size - 1,
                        self.cell_size - 1)
                if clist[y][x] == 0:
                    pygame.draw.rect(self.screen,
                                     pygame.Color('white'),
                                     rect)
                else:
                    pygame.draw.rect(self.screen,
                                     pygame.Color('green'),
                                     rect)

    def get_neighbours(self, cell: tuple) -> list:
        """ Вернуть список соседей для указанной ячейки

        :param cell: Позиция ячейки в сетке, задается кортежем вида (row, col)
        :return: Одномерный список ячеек, смежных к ячейке cell
        """
        neighbours = []
        row, col = cell
        for j in range(-1, 2):
            for i in range(-1, 2):
                if (0 <= row+j < self.cell_height) and (0 <= col+i < self.cell_width) and (i+j != i*j):
                    neighbours.append(self.clist[row+j][col+i])
        return neighbours

    def update_cell_list(self, cell_list: list) -> list:
        """ Выполнить один шаг игры.
        Обновление всех ячеек происходит одновременно. Функция возвращает
        новое игровое поле.
        :param cell_list: Игровое поле, представленное в виде матрицы
        :return: Обновленное игровое поле
        """
        new_clist = []
        for r in range(len(cell_list)):
            new_clist.append([])
            for c in range(len(cell_list[r])):
                neighbours = self.get_neighbours((r, c)).count(1)
                if (cell_list[r][c] == 0) and (neighbours == 3):
                    new_clist[r].append(1)
                elif (cell_list[r][c] == 1) and (2 <= neighbours <= 3):
                    new_clist[r].append(1)
                else:
                    new_clist[r].append(0)
        self.clist = new_clist
        return self.clist


def main():
    game = GameOfLife(640, 640, 5)
    game.run()


if __name__ == '__main__':
    main()
