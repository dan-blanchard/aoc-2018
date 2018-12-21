from collections import defaultdict, namedtuple
from copy import deepcopy
from operator import itemgetter

Line = namedtuple("Line", ["x", "y"])
WATER_SYMBOLS = ("+", "|", "~")
SPRING = (500, 0)
Grid = namedtuple("Grid", ["rows", "y_min", "y_max", "x_min", "x_max"])


def parse_puzzle(puzzle_input_file, spring=SPRING):
    grid = defaultdict(lambda: defaultdict(lambda: "."))
    global_y_min = float("inf")
    global_y_max = float("-inf")
    global_x_min = float("inf")
    global_x_max = float("-inf")
    with open(puzzle_input_file, "r") as puzzle_input:
        for line in puzzle_input:
            line = line.strip().replace("=", "='").replace(",", "',")
            line = eval(f"Line({line}')")
            x_range = tuple(int(x) for x in line.x.split(".."))
            x_min, x_max = (x_range[0], x_range[0]) if len(x_range) == 1 else x_range
            y_range = tuple(int(y) for y in line.y.split(".."))
            y_min, y_max = (y_range[0], y_range[0]) if len(y_range) == 1 else y_range
            global_y_min = min(global_y_min, y_min)
            global_y_max = max(global_y_max, y_max)
            global_x_min = min(global_x_min, x_min)
            global_x_max = max(global_x_max, x_max)
            for y in range(y_min, y_max + 1):
                for x in range(x_min, x_max + 1):
                    grid[y][x] = "#"
    grid[spring[1]][spring[0]] = "+"
    global_x_max += 1
    global_x_min -= 1
    return Grid(grid, global_y_min, global_y_max, global_x_min, global_x_max)


def print_grid(grid, spring=SPRING):
    for y in range(min(grid.y_min, SPRING[1]), grid.y_max + 1):
        row = grid.rows[y]
        for x in range(min(grid.x_min, SPRING[0]), grid.x_max + 1):
            print(row[x], end="")
        print()


def advance_water(grid, spring=SPRING, verbose=False):
    y_min = min(grid.y_min, SPRING[1])
    x_min = min(grid.x_min, SPRING[0])
    y_max = max(grid.y_max, SPRING[1])
    x_max = max(grid.x_max, SPRING[0])
    iteration = 0
    changed = True
    prev_lowest_change = y_min
    while changed:
        iteration += 1
        changed = False
        lowest_change = None
        # Set | when water is above
        for y in range(prev_lowest_change, y_max + 1):
            for x in range(x_min, x_max + 1):
                curr = grid.rows[y][x]
                if curr == "#":
                    continue
                above = grid.rows[y - 1][x]
                below = grid.rows[y + 1][x]
                left = grid.rows[y][x - 1]
                right = grid.rows[y][x + 1]
                if above in ("|", "+") and curr == ".":
                    curr = grid.rows[y][x] = "|"
                    if lowest_change is None:
                        lowest_change = y
                    changed = True
                if below in ("#", "~") and curr in WATER_SYMBOLS:
                    if left == ".":
                        left = grid.rows[y][x - 1] = "|"
                        changed = True
                        if lowest_change is None:
                            lowest_change = y
                    if right == ".":
                        right = grid.rows[y][x + 1] = "|"
                        changed = True
                        if lowest_change is None:
                            lowest_change = y

            # Scan for contained spots
            left_wall_x = None
            has_water = False
            for x in range(grid.x_min, grid.x_max + 1):
                below = grid.rows[y + 1][x]
                curr = grid.rows[y][x]
                if curr == "#" and below in ("#", "~"):
                    if left_wall_x is not None:
                        # actually found a left and right wall
                        for contained_x in range(left_wall_x + 1, x):
                            curr_contained = grid.rows[y][contained_x]
                            if has_water and curr_contained != "~":
                                grid.rows[y][contained_x] = "~"
                                if lowest_change is None:
                                    lowest_change = y
                                changed = True
                    left_wall_x = x
                    has_water = False
                elif below not in ("#", "~"):
                    left_wall_x = None
                if left_wall_x is not None and curr in WATER_SYMBOLS:
                    has_water = True

        prev_lowest_change = lowest_change - 1
        if verbose:
            print_grid(grid)
            print()
        elif iteration % 10 == 0:
            print(iteration, end="\r")
    print()


def count_water_tiles(grid, still_only=False):
    count = 0
    for y in range(grid.y_min, grid.y_max + 1):
        for x in range(grid.x_min, grid.x_max + 1):
            curr = grid.rows[y][x]
            if (not still_only and curr in WATER_SYMBOLS) or (
                still_only and curr == "~"
            ):
                count += 1

    return count
