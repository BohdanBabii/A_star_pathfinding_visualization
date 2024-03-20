import pygame
from node import Node
from config import GREY, WHITE

def make_grid(rows, width):
    """
    Creates a 2D grid of nodes.

    Args:
        rows (int): Number of rows in the grid.
        width (int): Width of the grid.

    Returns:
        list: 2D list representing the grid of nodes.
    """
    grid = []
    gap = width // rows  # Determines the size of each cell/square in the grid
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid(win, rows, width):
    """
    Draws grid lines on the game window.

    Args:
        win (pygame.Surface): Game window surface.
        rows (int): Number of rows in the grid.
        width (int): Width of the grid.

    Returns:
        None
    """
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    """
    Draws the entire grid and its contents on the game window.

    Args:
        win (pygame.Surface): Game window surface.
        grid (list): 2D list representing the grid of nodes.
        rows (int): Number of rows in the grid.
        width (int): Width of the grid.

    Returns:
        None
    """
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    """
    Converts mouse click position to grid coordinates.

    Args:
        pos (tuple): Mouse click position (x, y).
        rows (int): Number of rows in the grid.
        width (int): Width of the grid.

    Returns:
        tuple: Grid coordinates (row, col).
    """
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col
