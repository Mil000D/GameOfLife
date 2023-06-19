# Game Of Life

This repository contains an implementation of the Game Of Life, a cellular automaton devised by John Horton Conway in 1970.

The Game Of Life is a zero-player game, meaning that its evolution is determined by its initial state without the need for further input.

## Description

The Game of Life takes place on an infinite two-dimensional orthogonal grid of square cells. Each cell can be in one of two states: alive or dead. The game evolves through discrete time steps, where the state of each cell at the next generation is determined by its current state and the states of its eight neighboring cells.

The rules of the Game Of Life are as follows:

1. Any live cell with fewer than two live neighbors dies (underpopulation).
2. Any live cell with two or three live neighbors survives.
3. Any live cell with more than three live neighbors dies (overpopulation).
4. Any dead cell with exactly three live neighbors becomes a live cell (reproduction).

The program allows the user to create an initial configuration of live and dead cells and observe how it evolves over time. The boundaries of the grid have cyclic conditions, meaning that cells on the edges are considered neighbors with cells on the opposite edges.

## Usage

1. Run the program.
2. Modify the rules of the game if desired.
3. Input values such as size of the window or name of file for your initial configuration.
4. Click on the `Create Game Of Life` button.
5. Set the initial configuration of live and dead cells according to your preference.
6. Run the program.
7. Observe the evolution of the grid as the generations progress.

## Customization

The program allows for customization in several aspects:

- Initial Configuration: You can set the initial configuration of live and dead cells to create different patterns and observe their evolution. You can also save your initial configurations.
- Rules: You can modify the rules of the game to experiment with different behaviors and patterns.
- Grid Size: The size of the grid can be adjusted to fit different dimensions.
- Boundary Conditions: The program implements cyclic boundary conditions.
