from enum import Enum

class Direction(Enum):
    Left = "Left"
    Down = "Down"
    Right = "Right"
    Up = "Up"



class Key:
    Left = -1
    Down = -1
    Right = -1
    Up = -1
    Enter = 10
    
    @staticmethod
    def move_keys() -> list:
        return [Key.Left, Key.Down, Key.Right, Key.Up]

    @staticmethod
    def to_direction(key) -> Direction:
        if key not in Key.move_keys():
            raise Exception(f"Unable to convert key into direction: {key = }")

        return {
            Key.Left: Direction.Left,
            Key.Down: Direction.Down,
            Key.Right: Direction.Right,
            Key.Up: Direction.Up
        }[key]

class SnakeMove(Enum):
    Moved = 0
    Hit = 1
    Eat = 2