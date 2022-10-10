import time
import random

from src.Screen import create_screen, close
from src.Enums import Key, SnakeMove
from src.Snake import Snake


class GameState:

    def __init__(self, window_width, window_height) -> None:
        # initialize screen etc
        self._screen = create_screen()
        self._move_speed = 0.5
        self._win_height = window_height
        self._win_width = window_width
        self._snake = Snake(window_width=self._win_width,
                            window_height=self._win_height)
        self._apple_pos = None
        self.score = 0
        self._create_new_apple_pos()

    def set_keys(self) -> None:
        """
        Prompts and saves the arrow keys used to move the snake
        """

        def key_action(idx: int, key: int) -> None:
            if idx == 0: Key.Left = key
            elif idx == 1: Key.Right = key
            elif idx == 2: Key.Up = key # reverted in purpose
            elif idx == 3: Key.Down = key # reverted in purpose
            else: raise "Invalid key"


        key_prompts = ["LEFT", "RIGHT", "DOWN", "UP"]
        for i in range(len(key_prompts)):
            self._screen.addstr(self._win_height // 2 -
                                1, 2, f"Key {i + 1} / 4")
            self._screen.addstr(self._win_height // 2, 2,
                                f"Press key for moving mouse {key_prompts[i]}...{' ':<10}")
            self._screen.refresh()

            key = self._screen.getch()
            while key in Key.move_keys():
                self._screen.addstr(self._win_height // 2 + 1, 2,
                            f"Key is already assigned, please input a different one")
                self._screen.refresh()
                key = self._screen.getch()

            key_action(i, key)


            self._screen.addstr(self._win_height // 2, 2,
                                f"Press key for moving mouse {key_prompts[i]}... {key}")
            self._screen.addstr(self._win_height // 2 + 1, 2, f"{' ':<54}") # Remove the possible "key is already assigned..." message
            self._screen.refresh()
            time.sleep(0.5)

        # When keys are set, set nodelay for key inputs
        self._screen.nodelay(1)

    def run(self) -> None:
        exit = False
        # main loop
        while True:
            # update screen
            self._update_screen()

            # Wait for user input
            self._handle_user_input()

            move_res = self._snake.move(self._apple_pos)
            if move_res == SnakeMove.Hit:
                exit = self._restart()
                break

            if move_res == SnakeMove.Eat:
                # Create new apple
                self._create_new_apple_pos()
                # Make the worm go faster
                self._update_speed()
                self.score += 1
            elif move_res == SnakeMove.Moved:
                pass
            else:
                raise Exception(f"Invalid wormmove result {move_res = }")

        if not exit:
            self.run()

        close(self._screen)

    def _restart(self) -> bool:
        self._screen.addstr(self._win_height // 2, 2,
                            f"Press enter for new game, q to exit")
        self._screen.refresh()

        key = self._screen.getch()
        while key != ord('q') and key != Key.Enter:
            key = self._screen.getch()
            time.sleep(0.1)

        self._snake = Snake(window_width=self._win_width,
                            window_height=self._win_height)
        self._apple_pos = None
        self.score = 0
        self._create_new_apple_pos()
        return key == ord('q')

    def _update_screen(self) -> None:
        self._screen.clear()
        # draw the window
        self._screen.hline(0, 1, "_", self._win_width - 1)
        self._screen.hline(self._win_height, 1, "_", self._win_width - 1)

        self._screen.vline(1, 0, "|", self._win_height)
        self._screen.vline(1, self._win_width, "|", self._win_height)

        # Info
        # self._screen.addstr(self._win_height + 1, 0, f"Speed: ${self._move_speed}")
        self._screen.addstr(self._win_height + 1, 0, f"Score: {self.score}")

        # add +1 to both x and y for the walls to be at 0
        for (x, y) in self._snake.positions:
            self._screen.addstr(y + 1, x + 1, "#")

        self._screen.addstr(
            self._apple_pos[1] + 1, self._apple_pos[0] + 1, "o")

        self._screen.refresh()

    def _handle_user_input(self) -> None:
        start_time = time.time()
        while time.time() - start_time < self._move_speed:
            key = self._screen.getch()
            # Check if key is one direction keys
            if key in Key.move_keys():
                # Convert key into direction
                dir = Key.to_direction(key)
                # Apply to direction change
                self._snake.set_direction(dir)
                break

            time.sleep(0.05)

    def _create_new_apple_pos(self) -> None:
        worm_positions = self._snake.positions
        while True:
            self._apple_pos = (random.randint(
                0, self._win_width - 2), random.randint(0, self._win_height - 2))
            if self._apple_pos not in worm_positions:
                return

    def _update_speed(self):
        self._move_speed = max(self._move_speed * 0.95, 0.05)
