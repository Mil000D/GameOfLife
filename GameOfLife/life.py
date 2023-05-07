import pygame
from pygame import Surface


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
