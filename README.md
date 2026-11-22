# Sudoku Game

A small Sudoku game written in Python with Pygame.

The board is a standard 9x9 grid. At start, the program fills 27 cells by random search. Each given number has to be legal in its row, column, and 3x3 box, and each box is capped at three givens, so a finished opening has three givens in every box. You click a cell and type 1-9 to fill it. Given cells stay fixed. Given numbers are drawn in blue. Numbers you type are black, or red when the move is illegal.

## Features

- Fill cells from the keyboard. With a cell selected, the digits 1-9 write into that cell when it is not a given. A digit you already typed can be replaced by another digit.
- Invalid moves are marked in red and show "Error: Invalid number!". The illegal digit is stored on the board. The message stays up for about one second, then clears. The red digit stays until a later digit in that same cell passes the row, column, and box check. The selected cell is outlined in red whether or not the digit is illegal. The check counts every digit already on the board, including the digit in the selected cell, so typing that same digit again is reported as invalid.
- A Help button shows possible numbers for the selected cell, using an elimination check on the row, column, and box. The on-screen label is "Possible Numbers:". The list stays up for about one second. It is built from the board as it stands, so illegal digits already entered count as taken. Given cells yield an empty list. Select a cell first. With no selection, Help has no effect.

This is a short student project. The initial fill is random. This program is not a Sudoku solver or a difficulty-rated puzzle generator. The opening is not checked for a solution, or for a unique solution. The fill loop keeps sampling random cells until all 27 givens are placed, and that loop has no attempt limit.

## How to run

The main file name contains a space. Use Python 3.

```bash
git clone https://github.com/yemre345561/Sudoku-Game.git
cd Sudoku-Game
pip install -r requirements.txt
python "Sudoku Game.py"
```

Pygame is the only third-party dependency. It is listed in `requirements.txt`. `sys`, `random`, and `time` come from the Python standard library.
