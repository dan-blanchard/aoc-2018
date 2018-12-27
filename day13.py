from collections import defaultdict
from itertools import chain, cycle
from uuid import uuid4


SYMBOLS_TO_TUPS = {"^": (0, -1), "v": (0, 1), "<": (-1, 0), ">": (1, 0)}
TUPS_TO_SYMBOLS = {(0, -1): "^", (0, 1): "v", (-1, 0): "<", (1, 0): ">"}


class Cart:
    def __init__(self, *, x, y, facing, id=None):
        self.x = x
        self.y = y
        self.turn_cycle = cycle([(-1, 1), None, (1, -1)])
        self.facing = facing
        self.id = str(uuid4())

    def __repr__(self):
        return f"Cart(x={self.x}, y={self.y}, facing={self.facing}, id={self.id})"

    def __lt__(self, other):
        return (self.y, self.x) < (other.y, other.x)

    def __hash__(self):
        return hash(self.id)


def parse_puzzle(puzzle):
    puzzle = puzzle.splitlines()
    tracks = []
    carts = []

    for y, row in enumerate(puzzle):
        track_row = []
        for x, char in enumerate(row):
            if char not in SYMBOLS_TO_TUPS:
                track_char = char
            else:
                carts.append(Cart(x=x, y=y, facing=SYMBOLS_TO_TUPS[char]))
                if char == "<" or char == ">":
                    track_char = "-"
                else:
                    track_char = "|"
            track_row.append(track_char)
        tracks.append(tuple(track_row))
    tracks = tuple(tracks)
    return tracks, carts


def advance_carts(carts, tracks, remove_crashed=False):
    cart_positions = defaultdict(set)
    for cart in carts:
        cart_positions[(cart.x, cart.y)].add(cart)
    crashed = False
    for cart in sorted(carts):
        # Check for already crashed cart
        old_pos = (cart.x, cart.y)
        if len(cart_positions[old_pos]) > 1:
            continue
        else:
            cart_positions[old_pos].remove(cart)
        new_y = cart.y + cart.facing[1]
        new_x = cart.x + cart.facing[0]
        next_track = tracks[new_y][new_x]
        cart.y = new_y
        cart.x = new_x
        pos = (cart.x, cart.y)
        if pos in cart_positions:
            print(f"Crash at {pos}")
            crashed = True
        cart_positions[pos].add(cart)
        if next_track == "+":
            turn = next(cart.turn_cycle)
            if turn is not None:
                cart.facing = (cart.facing[1] * turn[1], cart.facing[0] * turn[0])
        elif next_track == "/":
            cart.facing = (cart.facing[1] * -1, cart.facing[0] * -1)
        elif next_track == "\\":
            cart.facing = (cart.facing[1], cart.facing[0])
        elif next_track != "|" and next_track != "-":
            raise ValueError(f"This should never happen. Got '{next_track}'")
    return (
        list(
            chain.from_iterable(
                cart_set
                for cart_set in cart_positions.values()
                if not remove_crashed or len(cart_set) == 1
            )
        ),
        crashed,
    )


def print_state(carts, tracks):
    cart_chars = {}
    for cart in carts:
        pos = (cart.x, cart.y)
        if pos not in cart_chars:
            cart_chars[pos] = TUPS_TO_SYMBOLS[cart.facing]
        else:
            cart_chars[pos] = "X"
    for y, track_row in enumerate(tracks):
        for x, track_char in enumerate(track_row):
            print(cart_chars.get((x, y), track_char), end="")
        print()


def find_first_crash(puzzle, verbose=False):
    tracks, carts = parse_puzzle(puzzle)
    crashed = False
    while not crashed:
        if verbose:
            print()
            print_state(carts, tracks)
        carts, crashed = advance_carts(carts, tracks, remove_crashed=False)
    if verbose:
        print()
        print_state(carts, tracks)


def find_last_cart(puzzle, verbose=False):
    tracks, carts = parse_puzzle(puzzle)
    while len(carts) > 1:
        if verbose:
            print()
            print_state(carts, tracks)
        carts = advance_carts(carts, tracks, remove_crashed=True)[0]
    return carts[0]
