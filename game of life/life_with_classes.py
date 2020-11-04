import pygame
from pygame.locals import *
import random
from copy import deepcopy
from pprint import pprint as pp


class GameOfLife:

    def __init__(self, width: int = 640,
                 height: int = 480,
                 cell_size: int = 10,
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

    def draw_cell_list(self, clist) -> None:
        """ Отображение списка клеток"""
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                rect = (x * self.cell_size + 1,
                        y * self.cell_size + 1,
                        self.cell_size - 1,
                        self.cell_size - 1)
                if clist.grid[y][x].is_alive() == 0:
                    pygame.draw.rect(self.screen,
                                     pygame.Color('white'),
                                     rect)
                else:
                    pygame.draw.rect(self.screen,
                                     pygame.Color('green'),
                                     rect)

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        self.clist = CellList(self.cell_height, self.cell_width, True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            # Отрисовка списка клеток
            self.draw_grid()
            self.draw_cell_list(self.clist)

            # Выполнение одного шага игры (обновление состояния ячеек)
            self.clist.update()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


class Cell:

    def __init__(self, row: int, col: int, state: bool = False) -> None:
        self.row = row
        self.col = col
        self.state = state

    def is_alive(self) -> bool:
        return self.state


class CellList:

    def __init__(self, nrows: int, ncols: int, randomize: bool = False) -> None:
        self.nrows = nrows
        self.ncols = ncols
        if randomize:
            self.grid = self.generate_grid(randomize=True)
        else:
            self.grid = self.generate_grid()

    def generate_grid(self, randomize: bool = False) -> list:
        if randomize:
            new_clist = [[Cell(y, x, random.randint(0, 1)) for x in range(self.ncols)] for y in range(self.nrows)]
        else:
            new_clist = [[Cell(y, x, 0) for x in range(self.ncols)] for y in range(self.nrows)]
        return new_clist

    def get_neighbours(self, cell: tuple) -> list:
        """ Вернуть список соседей для указанной ячейки"""
        neighbours = []
        row, col = cell.row, cell.col
        for j in range(-1, 2):
            for i in range(-1, 2):
                if (0 <= row+j < self.nrows) and (0 <= col+i < self.ncols) and ((i, j) != (0, 0)):
                    neighbours.append(self.grid[row+j][col+i])
        return neighbours

    def update(self):
        new_grid = deepcopy(self.grid)
        for cell in self:
            neighbours = self.get_neighbours(cell)
            neighbours_alive = sum(c.is_alive() for c in neighbours)
            if cell.is_alive() and (2 <= neighbours_alive <= 3):
                new_grid[cell.row][cell.col].state = 1
            elif neighbours_alive == 3:
                new_grid[cell.row][cell.col].state = 1
            else:
                new_grid[cell.row][cell.col].state = 0
        self.grid = new_grid
        return self

    def __iter__(self):
        self.iter_index = 0
        return self

    def __next__(self):
        if self.iter_index < self.nrows*self.ncols:
            cell = self.grid[self.iter_index // self.ncols][self.iter_index % self.ncols]
            self.iter_index += 1
            return cell
        else:
            raise StopIteration

    def __str__(self) -> str:
        s = []
        for cell in self:
            s.append(cell.is_alive())
        return str(s)

    @classmethod
    def from_file(cls, filename) -> list:
        f = open(filename, 'r')
        
        grid = [list(row) for row in f.read().split()]
        nrows = len(grid)
        ncols = len(grid[0])
        grid = [[Cell(y, x, int(grid[y][x])) for x in range(ncols)] for y in range(nrows)]
        cell_list = cls(nrows, ncols, False)
        cell_list.grid = grid
        f.close()
        return cell_list


def main():
    game = GameOfLife(640, 640, 40)
    game.run()


if __name__ == '__main__':
    main()
