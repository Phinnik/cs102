import random
import time
import threading
import multiprocessing
import asyncio


def read_sudoku(filename: str) -> list:
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(values: list) -> None:
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) +
              ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values: list, n: int) -> list:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    table = [values[i*n: n+i*n] for i in range(n)]
    return table


def get_row(values: list, pos: tuple) -> list:
    """ Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    row = values[pos[0]]
    return row


def get_col(values: list, pos: tuple) -> list:
    """ Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    col = [values[i][pos[1]] for i in range(len(values))]
    return col


def get_block(values: list, pos: tuple) -> list:
    """ Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    y, x = pos[0]//3*3, pos[1]//3*3
    block = [values[y + i // 3][x + i % 3] for i in range(9)]
    return block


def find_empty_positions(grid: list) -> tuple:
    """ Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['9', '8', '.']])
    (2, 2)
    """
    for ri, row in enumerate(grid):
        for ci, value in enumerate(row):
            if value == '.':
                return ri, ci
    return -1, -1


def find_possible_values(grid: list, pos: tuple) -> set:
    """ Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    impossibleValues = set(get_row(grid, pos) +
                           get_col(grid, pos) +
                           get_block(grid, pos))
    possibleValues = set('123456789') - impossibleValues
    return possibleValues


def solve(grid: list) -> list:
    """ Решение пазла, заданного в grid
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    emptyPos = find_empty_positions(grid)
    if emptyPos is None:
        return grid
    possibleValues = find_possible_values(grid, emptyPos)
    for val in possibleValues:
        grid[emptyPos[0]][emptyPos[1]] = val
        solution = solve(grid)
        if solution:
            return solution
        grid[emptyPos[0]][emptyPos[1]] = '.'
    return None


def check_solution(solution: list) -> bool:
    # TODO: Add doctests with bad puzzles
    goodSet = set('123456789')
    for i in range(len(solution)):
        if set(get_row(solution, (i, 0))) != goodSet:
            return False
        if set(get_col(solution, (0, i))) != goodSet:
            return False
        if set(get_block(solution, (i * 3 // 9, i * 3 % 9))) != goodSet:
            return False
    return True


def generate_sudoku(N: int) -> list:
    """ Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    grid = solve([['.'] * 9 for i in range(9)])
    N = 81 - min(81, max(0, N))
    while N:
        y, x = random.randint(0, 8), random.randint(0, 8)
        if grid[y][x] != '.':
            grid[y][x] = '.'
            N -= 1
    return grid


def run_solve(fname: str) -> bool:
    grid = read_sudoku(fname)
    start = time.time()
    solve(grid)
    end = time.time()
    print(f'{fname}: {end-start}')
    return True


if __name__ == "__main__":
    for fname in ('puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt'):
        p = multiprocessing.Process(target=run_solve, args=(fname,))
        p.start()
