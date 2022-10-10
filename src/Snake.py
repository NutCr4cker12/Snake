from src.Enums import Direction, SnakeMove

class Snake:

    def __init__(self, window_height: int, window_width: int) -> None:
        self._dir = Direction.Right
        self._temp_dir = None # temporary direction before the direction is actually applied
        self._lenght = 3
        self._apple_pending = False # Flag to append the worm from tail
        self._win_height = window_height
        self._win_width = window_width
        self._dir_horizontal = [Direction.Left, Direction.Right]
        self._dir_vertical = [Direction.Up, Direction.Down] 

        # list of (x, y) coorinates
        mid_x = self._win_width // 2
        mid_y = self._win_height // 2
        self.positions = [
            (mid_x - 2, mid_y), # tail ends
            (mid_x - 1, mid_y), # middle part
            (mid_x - 0, mid_y)  # head
        ]

    def set_direction(self, direction: Direction) -> None:
        # Don't change directions to reverse
        if not (direction in self._dir_horizontal and self._dir in self._dir_horizontal or \
            direction in self._dir_vertical and self._dir in self._dir_vertical):
            self._temp_dir = direction

    def move(self, apple_position) -> SnakeMove:
        """ 
            Moves the worm in the current direction for 1 pixel. 
            Returns
                WormMove.Move  - if worm moves succesfully and doesn't hit anything and doesn't eat aple
                WormMove.Hit   - if worm hit's anything
                WormMove.Eat   - if worm ate the apple
        """
        if self._temp_dir is not None:
            self._dir = self._temp_dir
            self._temp_dir = None

        # get the latest head position
        last_pos_x, last_pos_y = self.positions[-1]
        # create new position
        new_pos_x, new_pos_y = last_pos_x, last_pos_y
        if self._dir == Direction.Down:
            new_pos_y = last_pos_y - 1
        elif self._dir == Direction.Left:
            new_pos_x = last_pos_x - 1
        elif self._dir == Direction.Right:
            new_pos_x = last_pos_x + 1
        elif self._dir == Direction.Up:
            new_pos_y = last_pos_y + 1
        else:
            raise Exception(f"Current direction out of range {self._dir = }")

        # check if the worm will collide into walls
        if new_pos_x < 0 or new_pos_y < 0 or new_pos_x >= self._win_width - 1 or new_pos_y >= self._win_height:
            return SnakeMove.Hit
            
        new_pos = (new_pos_x, new_pos_y)

        # remove from tail only if the new position is on top of an apple
        if apple_position == new_pos:
            result = SnakeMove.Eat
        else:
            result = SnakeMove.Moved
            self.positions = self.positions[1:]

        # check if the worm will collide into itself
        if new_pos in self.positions:
            return SnakeMove.Hit

        # add the new location
        self.positions.append(new_pos)
        return result

