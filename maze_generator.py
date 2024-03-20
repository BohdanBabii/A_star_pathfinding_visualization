import random
from node import Node

def generate_random_maze(rows, cols):
    """
    Generates a random maze using Depth-First Search algorithm.

    Args:
        rows (int): Number of rows in the maze.
        cols (int): Number of columns in the maze.

    Returns:
        list: 2D list representing the generated maze.
    """
    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    def add_walls(x, y):
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 1:
                maze[nx][ny] = 0
                maze[nx - dx // 2][ny - dy // 2] = 0
                add_walls(nx, ny)

    start_x, start_y = random.randint(0, (rows - 1) // 2) * 2, random.randint(0, (cols - 1) // 2) * 2
    maze[start_x][start_y] = 0
    add_walls(start_x, start_y)

    return maze

def load_predefined_maze(grid, predefined_maze):
    """
    Loads a predefined maze onto the grid.

    Args:
        grid (list): 2D list representing the grid.
        predefined_maze (list): 2D list representing the predefined maze.

    Returns:
        None
    """
    for i, row in enumerate(predefined_maze):
        for j, cell in enumerate(row):
            node = grid[i][j]
            if cell == 1:
                node.make_barrier()

def clear_grid(grid):
    """
    Resets the grid by clearing all barriers and resets each node.

    Args:
        grid (list): 2D list representing the grid.

    Returns:
        None
    """
    for row in grid:
        for node in row:
            node.reset()
