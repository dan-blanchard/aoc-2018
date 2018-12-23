from collections import defaultdict, namedtuple
from copy import deepcopy
from concurrent.futures import ThreadPoolExecutor
from operator import itemgetter


def parse_puzzle(puzzle_input_file):
    with open(puzzle_input_file, "r") as puzzle_input:
        grid = tuple(tuple(line.strip()) for line in puzzle_input)
    return grid


def print_grid(grid):
    for row in grid:
        print("".join(row))
    print()


def advance_tile(args):
    grid, x, y, num_rows, num_cols = args
    new_val = grid[y][x]
    surrounding = "".join(
        grid[y + y_delta][x + x_delta]
        for y_delta in (-1, 0, 1)
        for x_delta in (-1, 0, 1)
        if not (x_delta == y_delta == 0)
        and 0 <= x + x_delta < num_cols
        and 0 <= y + y_delta < num_rows
    )
    if new_val == "." and surrounding.count("|") >= 3:
        new_val = "|"
    elif new_val == "|" and surrounding.count("#") >= 3:
        new_val = "#"
    elif new_val == "#" and ("#" not in surrounding or "|" not in surrounding):
        new_val = "."
    return new_val


def advance(grid, executor, minutes=10, verbose=False):
    num_rows = len(grid)
    num_cols = len(grid[0])
    if verbose:
        print("Initial grid")
        print_grid(grid)
    grids_to_minutes = {}
    minutes_to_grids = {}
    for minute in range(1, minutes + 1):
        if grid not in grids_to_minutes:
            grids_to_minutes[grid] = minute
            minutes_to_grids[minute] = grid
            grid = tuple(
                tuple(
                    executor.map(
                        advance_tile,
                        ((grid, x, row, num_rows, num_cols) for x in range(num_cols)),
                    )
                )
                for row in range(num_rows)
            )
            if verbose:
                print(f"After minute {minute}")
                print_grid(grid)
        # found repeat point, just use previous grid that will match end point
        else:
            print(f"Found repeat of {grids_to_minutes[grid]} at {minute}")
            cycle_start = grids_to_minutes[grid]
            cycle_length = minute - cycle_start
            final_grid_idx = cycle_start + ((minutes - cycle_start + 1) % cycle_length)
            print(f"Predicting {final_grid_idx} as final grid")
            grid = minutes_to_grids[final_grid_idx]
            if verbose:
                print(f"After minute {minutes}")
                print_grid(grid)
            break
    return grid


def calculate_value(grid):
    grid_str = "".join("".join(row) for row in grid)
    return grid_str.count("|") * grid_str.count("#")
