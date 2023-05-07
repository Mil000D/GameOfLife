import json
import pygame
from life import Life


class GameOfLife:
    def __init__(self, size_of_cell: int, window_size: tuple, ranges_alive: list, list_dead: list, name: str,
                 grid_alive: list = None) -> None:
        pygame.init()
        pygame.display.set_caption("Game Of Life")
        self.name = name
        self.window_size = window_size
        self.screen = pygame.display.set_mode(self.window_size)
        self.clock = pygame.time.Clock()
        self.fps = 5
        self.size_of_cell = size_of_cell
        self.grid = [[Life(i * size_of_cell, j * size_of_cell, size_of_cell, ranges_alive, list_dead, False)
                      for j in range(window_size[1] // size_of_cell)]
                     for i in range(window_size[0] // size_of_cell)]
        if grid_alive is not None:
            for elem in grid_alive:
                value1 = elem[0]
                value2 = elem[1]
                self.grid[value1][value2].is_alive = True
                self.grid[value1][value2].draw_life(self.screen)
        self.main_loop()

        pygame.quit()

    def main_loop(self) -> None:
        running = True
        start = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        start = True
                    if event.key == pygame.K_s and not start:
                        grid_alive = []
                        for i in range(self.window_size[0] // self.size_of_cell):
                            for j in range(self.window_size[1] // self.size_of_cell):
                                if self.grid[i][j].is_alive:
                                    grid_alive.append((i, j))

                        my_object = GameOfLifeDTO(self.size_of_cell, self.window_size, grid_alive)
                        json_string = json.dumps(my_object.__dict__, indent=4)

                        with open(f"initial_state/{self.name}.json", "w") as f:
                            f.write(json_string)

                if event.type == pygame.MOUSEBUTTONDOWN and not start:
                    if event.button == pygame.BUTTON_LEFT:
                        x, y = event.pos
                        i = x // self.size_of_cell
                        j = y // self.size_of_cell
                        if i < len(self.grid) and j < len(self.grid[0]):
                            self.grid[i][j].is_alive = True
                            self.grid[i][j].draw_life(self.screen)

                if event.type == pygame.MOUSEBUTTONDOWN and not start:
                    if event.button == pygame.BUTTON_RIGHT:
                        x, y = event.pos
                        i = x // self.size_of_cell
                        j = y // self.size_of_cell
                        if i < len(self.grid) and j < len(self.grid[0]):
                            self.grid[i][j].is_alive = False
                            self.grid[i][j].draw_life(self.screen)

            if start:
                self.screen.fill((0, 0, 0))
                for i in range(len(self.grid)):
                    for j in range(len(self.grid[i])):
                        self.grid[i][j].draw_life(self.screen)

                for i in range(len(self.grid)):
                    for j in range(len(self.grid[i])):
                        self.grid[i][j].update_state(self.grid)

                for i in range(len(self.grid)):
                    for j in range(len(self.grid[i])):
                        self.grid[i][j].update_is_alive()
            self.draw_grid()
            pygame.display.update()
            self.clock.tick(self.fps)

    def draw_grid(self) -> None:
        for i in range(len(self.grid) + 1):
            x = i * self.size_of_cell
            pygame.draw.line(self.screen, (105, 105, 105), (x, 0), (x, self.window_size[1]))

        for j in range(len(self.grid[0]) + 1):
            y = j * self.size_of_cell
            pygame.draw.line(self.screen, (105, 105, 105), (0, y), (self.window_size[0], y))


class GameOfLifeDTO:
    def __init__(self, size_of_cell: int, window_size: tuple, grid_alive: list) -> None:
        self.size_of_cell = size_of_cell
        self.window_size = window_size
        self.grid_alive = grid_alive
