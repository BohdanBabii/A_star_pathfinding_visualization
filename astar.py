import pygame
import math
import random
from queue import PriorityQueue

WIDTH = 1000
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

# Define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# Define a class for each node in the grid
class Node:
    def __init__(self, row, col, width, total_rows) -> None:
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self) -> tuple:
        """Return the position of the node"""
        return self.row, self.col

    def is_closed(self) -> bool:
        """Return if the node is closed"""
        return self.color == RED

    def is_open(self) -> bool:
        """Return if the node is open"""
        return self.color == GREEN

    def is_barrier(self) -> bool:
        """Return if the node is a barrier"""
        return self.color == BLACK

    def is_start(self) -> bool:
        """Return if the node is the start node"""
        return self.color == ORANGE

    def is_end(self) -> bool:
        """Return if the node is the end node"""
        return self.color == TURQUOISE

    def reset(self) -> None:
        """Reset the node"""
        self.color = WHITE

    def make_start(self) -> None:
        """Make the node the start node"""
        self.color = ORANGE

    def make_closed(self) -> None:
        """Close the node"""
        self.color = RED

    def make_open(self) -> None:
        """Open the node"""
        self.color = GREEN

    def make_barrier(self) -> None:
        """Make the node a barrier"""
        self.color = BLACK

    def make_end(self) -> None:
        """Make the node the end node"""
        self.color = TURQUOISE

    def make_path(self) -> None:
        """Make the node part of the path"""
        self.color = PURPLE

    def draw(self, win) -> None:
        """Draw the node"""
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid) -> None:
        """Update the neighbors of the node"""
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

def h(p1, p2) -> int:
    """Heuristic function (Manhattan distance)"""
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw) -> None:
    """Reconstruct the path"""
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def make_grid(rows, width) -> list[list[Node]]:
    """Create a grid of nodes"""
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid

def draw_grid(win, rows, width) -> None:
    """Draw grid lines"""
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width) -> None:
    """Draw the grid"""
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width) -> tuple[int, int]:
    """Get the position of a clicked node"""
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def algorithm(draw, grid, start, end) -> bool:
    """A* algorithm implementation"""
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

def clear_grid(grid):
    """Clear the grid"""
    for row in grid:
        for node in row:
            node.reset()



def load_predefined_maze(grid, predefined_maze):
    """Load a predefined maze configuration onto the grid"""
    for i in range(len(predefined_maze)):
        for j in range(len(predefined_maze[0])):
            node = grid[i][j]
            if predefined_maze[i][j] == 1:
                node.make_barrier()
            elif predefined_maze[i][j] == 2:
                node.make_start()
            elif predefined_maze[i][j] == 3:
                node.make_end()

def generate_random_maze(rows, cols):
    maze = [[1] * cols for _ in range(rows)]

    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols and maze[x][y] == 1

    def backtrack(x, y):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + 2*dx, y + 2*dy
            if is_valid(nx, ny):
                maze[nx][ny] = 0
                maze[x+dx][y+dy] = 0
                backtrack(nx, ny)

    start_x, start_y = random.randint(0, rows - 1), random.randint(0, cols - 1)
    maze[start_x][start_y] = 0
    backtrack(start_x, start_y)

    return maze

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None
    random_maze = generate_random_maze(ROWS, ROWS)

    # Convert the random maze to a format compatible with load_predefined_maze()
    predefined_maze = []
    for row in random_maze:
        row_data = []
        for cell in row:
            if cell == 0:
                row_data.append(0)  # Empty cell
            else:
                row_data.append(1)  # Barrier
        predefined_maze.append(row_data)

    load_predefined_maze(grid, predefined_maze)

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]

                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()
            elif pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                elif event.key == pygame.K_c:  # Clear the grid
                    clear_grid(grid)
                    start = None
                    end = None
                elif event.key == pygame.K_r:  # Generate new maze
                    clear_grid(grid)  # Clear the grid before generating a new maze
                    start = None  # Reset start node
                    end = None  # Reset end node
                    random_maze = generate_random_maze(ROWS, ROWS)
                    # Convert the random maze to a format compatible with load_predefined_maze()
                    predefined_maze = []
                    for row in random_maze:
                        row_data = []
                        for cell in row:
                            if cell == 0:
                                row_data.append(0)  # Empty cell
                            else:
                                row_data.append(1)  # Barrier
                        predefined_maze.append(row_data)

                    load_predefined_maze(grid, predefined_maze)

    pygame.quit()

main(WIN, WIDTH)
