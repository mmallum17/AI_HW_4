import maze_navigation.constants as constants
import random
import copy
from maze_navigation.mdp import Mdp


class ReinforcementLearning:

    def __init__(self, maze_grid):
        self.maze_grid = copy.deepcopy(maze_grid)
        self.init_util()

    def init_util(self):
        cols = len(self.maze_grid)
        rows = len(self.maze_grid[0])

        for c in range(cols):
            for r in range(rows):
                state = self.maze_grid[c][r]
                if state.terminal:
                    state.util = state.reward
                elif state.obstacle:
                    state.util = None
                else:
                    state.util = 0

    def get_init_pos(self):
        col_size = len(self.maze_grid)
        row_size = len(self.maze_grid[0])
        init_col = None
        init_row = None
        valid = False

        while not valid:
            init_col = random.randint(0, col_size - 1)
            init_row = random.randint(0, row_size - 1)

            if not self.maze_grid[init_col][init_row].terminal and not self.maze_grid[init_col][init_row].obstacle:
                valid = True

        return init_col, init_row

    def simulate_move(self, col, row, action):
        result_col = None
        result_row = None
        action_taken = None

        random_num = random.randint(0, 9)

        if action == constants.UP:
            if random_num <= 7:
                result_col, result_row = self.get_up_state(col, row)
                action_taken = constants.UP
            elif random_num == 8:
                result_col, result_row = self.get_left_state(col, row)
                action_taken = constants.LEFT
            else:
                result_col, result_row = self.get_right_state(col, row)
                action_taken = constants.RIGHT
        elif action == constants.DOWN:
            if random_num <= 7:
                result_col, result_row = self.get_down_state(col, row)
                action_taken = constants.DOWN
            elif random_num == 8:
                result_col, result_row = self.get_left_state(col, row)
                action_taken = constants.LEFT
            else:
                result_col, result_row = self.get_right_state(col, row)
                action_taken = constants.RIGHT
        elif action == constants.LEFT:
            if random_num <= 7:
                result_col, result_row = self.get_left_state(col, row)
                action_taken = constants.LEFT
            elif random_num == 8:
                result_col, result_row = self.get_up_state(col, row)
                action_taken = constants.UP
            else:
                result_col, result_row = self.get_down_state(col, row)
                action_taken = constants.DOWN
        elif action == constants.RIGHT:
            if random_num <= 7:
                result_col, result_row = self.get_right_state(col, row)
                action_taken = constants.RIGHT
            elif random_num == 8:
                result_col, result_row = self.get_up_state(col, row)
                action_taken = constants.UP
            else:
                result_col, result_row = self.get_down_state(col, row)
                action_taken = constants.DOWN

        return result_col, result_row, action_taken

    def get_up_state(self, col, row):
        row_size = len(self.maze_grid[0])

        # Get location if going up
        if row >= row_size - 1 or self.maze_grid[col][row + 1].obstacle:
            up_state = col, row
        else:
            up_state = col, row + 1
        return up_state

    def get_down_state(self, col, row):
        # Get location if going down
        if row <= 0 or self.maze_grid[col][row - 1].obstacle:
            down_state = col, row
        else:
            down_state = col, row - 1
        return down_state

    def get_left_state(self, col, row):
        # Get location if going left
        if col <= 0 or self.maze_grid[col - 1][row].obstacle:
            left_state = col, row
        else:
            left_state = col - 1, row
        return left_state

    def get_right_state(self, col, row):
        col_size = len(self.maze_grid)

        # Get location if going right
        if col >= col_size - 1 or self.maze_grid[col + 1][row].obstacle:
            right_state = col, row
        else:
            right_state = col + 1, row
        return right_state
