from enum import Enum

class Direction(Enum):
    Left = "Left"
    Down = "Down"
    Right = "Right"
    Up = "Up"

class Key(Enum):
    Left = 452
    Down = 450 # reverted in purpose
    Right = 454
    Up = 456
    Enter = 10

    @staticmethod
    def to_direction(key) -> Direction:
        if key not in Key._value2member_map_:
            raise Exception(f"Unable to convert key into direction: {key = }")

        return {
            Key.Left.value: Direction.Left,
            Key.Down.value: Direction.Down,
            Key.Right.value: Direction.Right,
            Key.Up.value: Direction.Up
        }[key]

class SnakeMove(Enum):
    Moved = 0
    Hit = 1
    Eat = 2