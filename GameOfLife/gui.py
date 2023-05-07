import json
import os
import tkinter as tk
from tkinter import ttk
from game_of_life import GameOfLife, GameOfLifeDTO


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

        label1 = ttk.Label(root, text="Enter size of single cell")
        label1.pack()

        self.text_field1 = ttk.Entry(root)
        self.text_field1.pack()

        label2 = ttk.Label(root, text="Enter width of frame")
        label2.pack()

        self.text_field2 = ttk.Entry(root)
        self.text_field2.pack()

        label3 = ttk.Label(root, text="Enter height of frame")
        label3.pack()

        self.text_field3 = ttk.Entry(root)
        self.text_field3.pack()

        label4 = ttk.Label(root, text="Name your file for storing initial state")
        label4.pack()

        self.text_field4 = ttk.Entry(root)
        self.text_field4.pack()

        numbers_frame = ttk.Frame(root)
        for i in range(0, 9):
            label = ttk.Label(numbers_frame, text=f"         {i}") if i == 0 else ttk.Label(numbers_frame, text=f"{i}")
            label.pack(side="left", padx=8)
        numbers_frame.pack()

        tick_frame_dead = ttk.Frame(root)
        self.list_tick_dead = self.create_ticks(tick_frame_dead, True)

        tick_frame_alive = ttk.Frame(root)
        self.list_tick_alive = []
        self.list_tick_alive = self.create_ticks(tick_frame_alive, False)

        self.label5 = ttk.Label(root, text="")
        self.label5.pack()

        button = ttk.Button(root, text="Create Game Of Life", command=self.create_life)
        button.pack()

        button_help = ttk.Button(root, text="Help", command=self.create_help_window)
        button_help.pack()

        separator = ttk.Separator(root, orient="horizontal")
        separator.pack(fill="x")

        self.label6 = ttk.Label(root, text="Choose your initial state")
        self.label6.pack()

        root_path = "initial_state"
        files = []
        for dirpath, dirnames, filenames in os.walk(root_path):
            for file in filenames:
                files.append(os.path.join(file))

        listbox = tk.Listbox(root)
        listbox.bind("<Double-Button-1>", self.click_handler)
        listbox.pack()

        for i in files:
            listbox.insert(tk.END, i)

        root.mainloop()

    def create_ticks(self, tick_frame: ttk.Frame, dead: bool) -> list:
        list_tick = []
        label = ttk.Label(tick_frame, text="Dead") if dead else ttk.Label(tick_frame, text="Alive")
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

    def click_handler(self, event) -> None:
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
        GameOfLife(size_of_cell, tuple(window_size), create_ranges(list_alive),
                   list_dead, name_without_extension, game_of_life_dto.grid_alive)

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

    def create_help_window(self) -> None:
        help_window = tk.Tk()
        help_window.title("Help")
        notebook = ttk.Notebook(help_window)

        text = tk.Text(notebook)
        text.insert(tk.END, "Game Of Life\n\n")
        text.insert(tk.END, "To create a game of life you can either create your own\n"
                            "by providing necessary parameters and clicking 'Create Game Of Life'\n"
                            "or use a file from the list in which an initial state is stored.\n"
                            "My version allows to change rules of Life as desired, you can change them\n"
                            "by checking or unchecking ticks.\n\n")
        text.insert(tk.END, "To add a living cell in an initial state you can click on a shown grid\n"
                            "with a left button of a mouse, pressed ones should become white.\n"
                            "To change the state of living cell to dead you can press a right button,\n"
                            "alive cells should become dead by becoming black again\n"
                            "(it only works at it's initial state - after start it does not work anymore).\n\n")
        text.insert(tk.END, "To save your initial state to a json file you can press 's' key on your keyboard\n"
                            "and it should automatically create/update it inside your initial_state folder.\n"
                            "If you don't want to save your initial state you can just press 'space' key\n"
                            "on your keyboard and observe how your life is evolving")
        text.config(state="disabled")
        text.pack()

        notebook.pack()
