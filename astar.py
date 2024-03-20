import pygame
from queue import PriorityQueue
from config import PURPLE

def h(p1, p2):
    """
    Heuristic function to estimate the distance between two points using Manhattan distance.

    Args:
        p1 (tuple): Coordinates of the first point (x, y).
        p2 (tuple): Coordinates of the second point (x, y).

    Returns:
        int: Manhattan distance between the two points.
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    """
    Reconstructs the path from start to end by following the came_from dictionary.

    Args:
        came_from (dict): Dictionary containing the path information.
        current (Node): Current node to reconstruct the path from.
        draw (function): Function to draw the grid.

    Returns:
        None
    """
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    """
    A* algorithm to find the shortest path from start to end on a given grid.

    Args:
        draw (function): Function to draw the grid.
        grid (2D list): 2D list representing the grid.
        start (Node): Starting node of the path.
        end (Node): Ending node of the path.

    Returns:
        bool: True if path is found, False otherwise.
    """
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False
