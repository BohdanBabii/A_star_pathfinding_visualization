import pygame
from node import Node
from draw import make_grid, draw, get_clicked_pos
from maze_generator import generate_random_maze, load_predefined_maze, clear_grid
from astar import algorithm
from config import WIDTH

def main(win, width):
    """
    Main function to run the A* pathfinding algorithm visualization.

    Args:
        win (pygame.Surface): Pygame window surface.
        width (int): Width of the window.

    Returns:
        None
    """
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
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

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    clear_grid(grid)

                if event.key == pygame.K_r:
                    start = None
                    end = None
                    clear_grid(grid)
                    predefined_maze = generate_random_maze(ROWS, ROWS)
                    load_predefined_maze(grid, predefined_maze)

    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("A* Path Finding Algorithm")
    main(WIN, WIDTH)
