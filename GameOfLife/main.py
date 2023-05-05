import json
import os
import pygame
from pygame import Surface
import tkinter as tk


def create_ranges(list_alive: list) -> list:
    list_alive = list(filter(lambda x: x != -1, list_alive))
    list_of_ranges = []
    if len(list_alive) == 0:
        list_of_ranges.append((-1, 9))
    for i in range(len(list_alive)):
        if list_alive[i] == 0 and len(list_alive) == 1:
            list_of_ranges.append((list_alive[i], 9))
            break
        elif list_alive[i] == 8 and len(list_alive) == 1:
            list_of_ranges.append((-1, list_alive[i]))
            break
        elif len(list_alive) == 1:
            list_of_ranges.append((-1, list_alive[i]))
            list_of_ranges.append((list_alive[i], 9))
            break
        elif i == 0 and list_alive[i] != 0:
            list_of_ranges.append((-1, list_alive[i]))
        elif i + 1 == len(list_alive) and i == 8:
            break
        elif i + 1 == len(list_alive) and i != 8:
            list_of_ranges.append((list_alive[i], 9))
            break
        list_of_ranges.append((list_alive[i], list_alive[i + 1]))
    return list_of_ranges


class GUI:
    def __init__(self) -> None:
        root = tk.Tk()
        root.title("Game Of Life")

        label1 = tk.Label(root, text="Enter size of single cell")
        label1.pack()

        self.text_field1 = tk.Entry(root)
        self.text_field1.pack()

        label2 = tk.Label(root, text="Enter width of frame")
        label2.pack()

        self.text_field2 = tk.Entry(root)
        self.text_field2.pack()

        label3 = tk.Label(root, text="Enter height of frame")
        label3.pack()

        self.text_field3 = tk.Entry(root)
        self.text_field3.pack()

        label4 = tk.Label(root, text="Name your file for storing initial state")
        label4.pack()

        self.text_field4 = tk.Entry(root)
        self.text_field4.pack()

        numbers_frame = tk.Frame(root)
        for i in range(0, 9):
            label = tk.Label(numbers_frame, text=f"         {i}") if i == 0 else tk.Label(numbers_frame, text=f"{i}")
            label.pack(side="left", padx=8)
        numbers_frame.pack()

        tick_frame_dead = tk.Frame(root)
        self.list_tick_dead = self.create_ticks(tick_frame_dead, True)

        tick_frame_alive = tk.Frame(root)
        self.list_tick_alive = []
        self.list_tick_alive = self.create_ticks(tick_frame_alive, False)

        self.label5 = tk.Label(root, text="")
        self.label5.pack()

        button = tk.Button(root, text="Create Game Of Life", command=self.create_life)
        button.pack()
        root_path = "initial_state"

        files = []
        for dirpath, dirnames, filenames in os.walk(root_path):
            for file in filenames:
                files.append(os.path.join(file))

        listbox = tk.Listbox(root)
        listbox.bind("<Double-Button-1>", self.click_handler)
        listbox.pack()

        for i in files:
            listbox.insert("end", i)

        root.mainloop()

    def create_ticks(self, tick_frame: tk.Frame, dead: bool) -> list:
        list_tick = []
        label = tk.Label(tick_frame, text="Dead") if dead else tk.Label(tick_frame, text="Alive")
        label.pack(side="left")
        for i in range(0, 9):
            tick_var = tk.BooleanVar(value=True if (dead and i == 3) or not dead and (i == 2 or i == 3) else False)
            tick = tk.Checkbutton(tick_frame, variable=tick_var)
            tick.pack(side="left")
            list_tick.append(tick_var)
        tick_frame.pack()
        return list_tick

    def create_life(self) -> None:
        try:
            size_of_cell = int(self.text_field1.get())
            window_size = [int(self.text_field2.get()), int(self.text_field3.get())]
            if size_of_cell not in (5, 20):
                size_of_cell = 20

            if window_size[0] not in range(100, 1600) or window_size[1] not in range(100, 800):
                window_size[0] = 1600
                window_size[1] = 800

            list_dead, list_alive = self.create_lists()

            name = self.text_field4.get()

            if len(name) == 0:
                raise ValueError
            GameOfLife(size_of_cell, tuple(window_size), create_ranges(list_alive), list_dead, self.text_field4.get())
        except ValueError:
            self.label5.config(text="Try again with different values")

    def click_handler(self, event):
        index = event.widget.curselection()[0]
        name = event.widget.get(index)
        file = f"initial_state/{name}"
        with open(file, "r") as f:
            data_dict = json.load(f)

        game_of_life_dto = GameOfLifeDTO(**data_dict)
        size_of_cell = game_of_life_dto.size_of_cell
        window_size = game_of_life_dto.window_size
        list_dead, list_alive = self.create_lists()

        name, extension = os.path.splitext(file)
        name_without_extension = name.split("/")[-1]
        GameOfLife(size_of_cell, tuple(window_size), create_ranges(list_alive), list_dead, name_without_extension, game_of_life_dto.grid_alive)

    def create_lists(self) -> tuple:
        list_dead = []
        for i in range(len(self.list_tick_dead)):
            if self.list_tick_dead[i].get():
                list_dead.append(i)
            else:
                list_dead.append(-1)

        list_alive = []
        for i in range(len(self.list_tick_alive)):
            if self.list_tick_alive[i].get():
                list_alive.append(i)
            else:
                list_alive.append(-1)
        return list_dead, list_alive


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


class Life:
    def __init__(self, x: int, y: int, size: int, ranges_alive: list, list_dead: list, is_alive: bool) -> None:
        self.x = x
        self.y = y
        self.size = size
        self.is_alive = is_alive
        self.next_state = None
        self.ranges_alive = ranges_alive
        self.list_dead = list(filter(lambda x: x != -1, list_dead))

    def draw_life(self, window: Surface) -> None:
        color = (255, 255, 255) if self.is_alive else (0, 0, 0)
        position = (self.x, self.y)
        size = (self.size, self.size)
        if self.is_alive:
            pygame.draw.rect(window, color, pygame.Rect(position, size))
        else:
            pygame.draw.rect(window, color, pygame.Rect(position, size))

    def update_state(self, board: list) -> None:
        live_neighbors = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                x = self.x // self.size + i
                y = self.y // self.size + j
                if x >= len(board):
                    x = 0
                if y >= len(board[0]):
                    y = 0
                if board[x][y].is_alive:
                    live_neighbors += 1
        truth_list_alive = [(elem[0] < live_neighbors < elem[1]) for elem in self.ranges_alive]
        truth_list_dead = [live_neighbors == elem for elem in self.list_dead]
        if self.is_alive and any(truth_list_alive):
            self.next_state = False
        elif not self.is_alive and any(truth_list_dead):
            self.next_state = True
        else:
            self.next_state = self.is_alive

    def update_is_alive(self) -> None:
        self.is_alive = self.next_state
        self.next_state = None


class GameOfLifeDTO:
    def __init__(self, size_of_cell: int, window_size: tuple, grid_alive: list) -> None:
        self.size_of_cell = size_of_cell
        self.window_size = window_size
        self.grid_alive = grid_alive


GUI()
