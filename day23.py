from collections import Counter, defaultdict, deque, namedtuple
from copy import deepcopy
from operator import itemgetter

Line = namedtuple("Line", ["pos", "r"])
Space = namedtuple("Space", ["dims", "mins", "maxes"])


def defaultdict_int():
    return defaultdict(int)


def defaultdict_dict():
    return defaultdict(dict)


def defaultdict_defaultdict_int():
    return defaultdict(defaultdict_int)


def parse_puzzle(puzzle_input_file):
    dims = defaultdict(defaultdict_dict)
    mins = [float("inf")] * 3
    maxes = [float("-inf")] * 3
    with open(puzzle_input_file, "r") as puzzle_input:
        for line in puzzle_input:
            line = line.strip().replace("<", "(").replace(">", ")")
            line = eval(f"Line({line})")
            for dim, val in enumerate(line.pos):
                mins[dim] = min(mins[dim], val)
                maxes[dim] = max(maxes[dim], val)
            dims[line.pos[0]][line.pos[1]][line.pos[2]] = line.r
    return Space(dims, mins, maxes)


def find_strongest_bot(space):
    largest_radius = float("-inf")
    coords = None
    for x, y_dim in space.dims.items():
        for y, z_dim in y_dim.items():
            for z, radius in z_dim.items():
                if radius > largest_radius:
                    largest_radius = radius
                    coords = (x, y, z)
    return coords, largest_radius


def count_bots_in_range(space, coords, radius, verbose=False):
    x1, y1, z1 = coords
    num_in_range = 0
    valid_x_range = set(range(x1 - radius, x1 + radius + 1))
    valid_y_range = set(range(y1 - radius, y1 + radius + 1))
    valid_z_range = set(range(z1 - radius, z1 + radius + 1))
    for x2, y_dim in space.dims.items():
        if x2 in valid_x_range:
            for y2, z_dim in y_dim.items():
                if y2 in valid_y_range:
                    for z2 in z_dim.keys():
                        if z2 in valid_z_range:
                            dist = abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)
                            in_range = dist <= radius
                            if verbose:
                                print(
                                    f"The nanobot at {x2},{y2},{z2} is distance {dist} away, and so it is {'in range' if in_range else 'NOT in range'}."
                                )
                            if in_range:
                                num_in_range += 1
    return num_in_range


def get_bot_range_coords(space, x1, y1, z1, radius):
    range_coords = list()
    for x2 in range(x1 - radius, x1 + radius + 1):
        x_dist = abs(x1 - x2)
        for y2 in range(y1 - radius, y1 + radius + 1):
            y_dist = abs(y1 - y2)
            if x_dist + y_dist <= radius:
                for z2 in range(z1 - radius, z1 + radius + 1):
                    dist = x_dist + y_dist + abs(z1 - z2)
                    if dist <= radius:
                        range_coords.append((x2, y2, z2))
    return range_coords


def find_best_spot(space, verbose=False):
    bot_ranges = []
    common_coords = Counter()
    for x, y_dim in space.dims.items():
        for y, z_dim in y_dim.items():
            for z, radius in z_dim.items():
                if verbose:
                    print(f"Calculating range coords for {x, y, z}", flush=True)
                bot_ranges.append(get_bot_range_coords(space, x, y, z, radius))
    if verbose:
        print("Calculating common coords...", end="", flush=True)
    for range in bot_ranges:
        if verbose:
            print(".", end="", flush=True)
        for coords in range:
            common_coords[coords] += 1
    if verbose:
        print()

    best_spot, prev_count = common_coords.most_common(1)[0]
    for coords, count in common_coords.most_common(None):
        if count != prev_count:
            break
        if sum(abs(i) for i in coords) < sum(abs(i) for i in best_spot):
            best_spot == coords
    return best_spot
