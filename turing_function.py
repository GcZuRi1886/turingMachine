from enum import Enum

EMPTY = "_"

def detect_symbol(symbol):
    if symbol == "0":
        return "0"
    elif symbol == "00":
        return "1"
    elif symbol == "000":
        return EMPTY
    else:
        raise ValueError(f"Invalid symbol: {symbol}")

class TuringFunction:
    def __init__(self, state, next_state, move_direction, write_symbol, read_symbol):
        self.state = len(state)
        self.next_state = len(next_state)
        self.move_direction = MoveDirection.LEFT if move_direction == '0' else MoveDirection.RIGHT
        self.write_symbol = detect_symbol(write_symbol)
        self.read_symbol = detect_symbol(read_symbol)

    def get_function_by_symbol(self, symbol):
        if self.read_symbol == symbol:
            return self
        return None


class MoveDirection(Enum):
    LEFT = -1
    RIGHT = 1