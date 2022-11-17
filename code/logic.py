"""logic.py: Manage the overall game logic."""

import copy
import random
import pygame as pg
import os


def merge(line, game=None):
    """Merge a single row, just like pressing "left" in 2048."""
    merged = []
    last_num = None
    for num in line:
        if num:
            if last_num is None:
                last_num = num
            elif num == last_num:
                # Merge 2 x 131072 into 2, just for fun
                new_num = 2 if last_num == 131072 else last_num * 2
                merged.append(new_num)
                if game:
                    game.score += last_num * 2
                last_num = None
            else:
                merged.append(last_num)
                last_num = num
    if last_num is not None:
        merged.append(last_num)
    merged += [0] * (len(line) - len(merged))

    return merged


def move_up(grid, game=None):
    """Merge each column upwards."""
    grid_size = len(grid)
    for i in range(grid_size):
        column = merge([row[i] for row in grid], game)
        for j in range(grid_size):
            grid[j][i] = column[j]


def move_right(grid, game=None):
    """Merge each row to the right."""
    for i, row in enumerate(grid):
        grid[i] = merge(row[::-1], game)[::-1]


def move_down(grid, game=None):
    """Merge each row downwards."""
    grid_size = len(grid)
    for i in range(grid_size):
        column = merge([row[i] for row in grid][::-1], game)[::-1]
        for j in range(grid_size):
            grid[j][i] = column[j]


def move_left(grid, game=None):
    """Merge each row to the left."""
    for i, row in enumerate(grid):
        grid[i] = merge(row, game)


def move_board(game, direction):
    """Move board into a given direction and create new number if board has
    changed."""
    game.temp_grid = copy.deepcopy(game.grid)

    if direction == "up":
        move_up(game.grid, game)
    elif direction == "right":
        move_right(game.grid, game)
    elif direction == "down":
        move_down(game.grid, game)
    elif direction == "left":
        move_left(game.grid, game)

    if game.grid != game.temp_grid:
        new_number(game.grid)


def new_number(grid):
    """Create a new number on the grid."""
    grid_size = len(grid)
    y, x = random.randrange(0, grid_size), random.randrange(0, grid_size)
    # If the random position is empty, else repeat function.
    if not grid[y][x]:
        # 90% probability for 2, 10% for 4.
        grid[y][x] = random.choice([2] * 9 + [4])
    else:
        new_number(grid)


def check_game_over(game):
    """Check if board is full and no moves are possible."""
    if all(all(row) for row in game.grid):
        temp_grid = copy.deepcopy(game.grid)
        move_up(temp_grid)
        move_right(temp_grid)
        move_down(temp_grid)
        move_left(temp_grid)
        if temp_grid == game.grid:
            game.phase = "game_over"


def check_win(game):
    """Check if tile 2048 is anywhere on the grid and tell the game event
    loop that game is won."""
    if not game.won:
        if any(2048 in row for row in game.grid):
            game.phase = "win"
            game.won = True


def save_score(score):
    f = open("high_score.txt", "w")
    f.write(str(score))
    f.close()


def read_score():
    f = open(os.path.join("high_score.txt"))
    score = int(f.read())
    f.close()
    return score


def update_high_score(game):
    """Updates and saves high score if current score is > high score."""
    if game.score > game.high_score:
        game.high_score = game.score
        save_score(game.score)


def new_game(game):
    # Reset score, won flag and phase
    game.score = 0
    game.won = False
    game.phase = "play"

    # Reset tiles
    grid_size = len(game.grid)
    for y in range(grid_size):
        for x in range(grid_size):
            game.grid[y][x] = 0

    # Make 2 new tiles
    new_number(game.grid)
    new_number(game.grid)


def button_hovered(btn_pos):
    """Checks if button with given position is currently hovered."""
    mouse_pos = pg.mouse.get_pos()
    collide_x = btn_pos[0][0] <= mouse_pos[0] <= btn_pos[0][1]
    collide_y = btn_pos[1][0] <= mouse_pos[1] <= btn_pos[1][1]
    return collide_x and collide_y


def shorten(n):
    """Shortens an integer to max 9 digits using scientific notation."""
    e = 0
    display = str(n)
    while len(display) > 9:
        n //= 10
        e += 1
        display = f"{n}e{e}"
    return display
