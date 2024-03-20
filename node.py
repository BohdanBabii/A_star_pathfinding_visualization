import pygame
from config import WHITE, RED, GREEN, BLACK, ORANGE, TURQUOISE, PURPLE

class Node:
    def __init__(self, row, col, width, total_rows):
        """
        Initializes a Node object.

        Args:
            row (int): Row index of the node.
            col (int): Column index of the node.
            width (int): Width of the node (square).
            total_rows (int): Total number of rows in the grid.

        Attributes:
            row (int): Row index of the node.
            col (int): Column index of the node.
            x (int): x-coordinate of the node's top-left corner.
            y (int): y-coordinate of the node's top-left corner.
            color (tuple): RGB color of the node.
            neighbors (list): List of neighboring nodes.
            width (int): Width of the node.
            total_rows (int): Total number of rows in the grid.
        """
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        """
        Returns the position of the node in the grid.

        Returns:
            tuple: Row and column indices of the node.
        """
        return self.row, self.col

    def is_closed(self):
        """
        Checks if the node is marked as closed.

        Returns:
            bool: True if the node is marked as closed, False otherwise.
        """
        return self.color == RED

    def is_open(self):
        """
        Checks if the node is marked as open.

        Returns:
            bool: True if the node is marked as open, False otherwise.
        """
        return self.color == GREEN

    def is_barrier(self):
        """
        Checks if the node is marked as a barrier.

        Returns:
            bool: True if the node is marked as a barrier, False otherwise.
        """
        return self.color == BLACK

    def is_start(self):
        """
        Checks if the node is marked as the start node.

        Returns:
            bool: True if the node is marked as the start node, False otherwise.
        """
        return self.color == ORANGE

    def is_end(self):
        """
        Checks if the node is marked as the end node.

        Returns:
            bool: True if the node is marked as the end node, False otherwise.
        """
        return self.color == TURQUOISE

    def reset(self):
        """Resets the color of the node to white."""
        self.color = WHITE

    def make_start(self):
        """Marks the node as the start node."""
        self.color = ORANGE

    def make_closed(self):
        """Marks the node as closed."""
        self.color = RED

    def make_open(self):
        """Marks the node as open."""
        self.color = GREEN

    def make_barrier(self):
        """Marks the node as a barrier."""
        self.color = BLACK

    def make_end(self):
        """Marks the node as the end node."""
        self.color = TURQUOISE

    def make_path(self):
        """Marks the node as part of the path."""
        self.color = PURPLE

    def draw(self, win):
        """Draws the node on the screen."""
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        """
        Updates the list of neighboring nodes.

        Args:
            grid (list): 2D list representing the grid.

        Returns:
            None
        """
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        """
        Overrides the less than operator for Node objects.

        Args:
            other (Node): Another Node object to compare with.

        Returns:
            bool: Always returns False.
        """
        return False
