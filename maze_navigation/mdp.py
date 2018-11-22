import random
import copy
import maze_navigation.constants as constants
# from maze_navigation.maze import Maze


class Mdp:

    gamma = 1

    def __init__(self, maze_grid):
        self.maze_grid = copy.deepcopy(maze_grid)

        # self.init_policy()
        # self.init_util()

    def init_policy(self):
        cols = len(self.maze_grid)
        rows = len(self.maze_grid[0])

        for c in range(cols):
            for r in range(rows):
                state = self.maze_grid[c][r]
                if state.terminal:
                    state.policy = constants.TERMINAL
                elif state.obstacle:
                    state.policy = constants.OBSTACLE
                else:
                    state.policy = random.randint(0, 3)

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

    def policy_iteration(self):
        cols = len(self.maze_grid)
        rows = len(self.maze_grid[0])

        while True:
            new_maze_grid = self.evaluate_policy()
            self.maze_grid = copy.deepcopy(new_maze_grid)
            # self.display_results()
            unchanged = True

            for c in range(cols):
                for r in range(rows):
                    state = self.maze_grid[c][r]

                    if not state.terminal and not state.obstacle:
                        new_util, max_action = self.calc_new_util(c, r)
                        if new_util > state.util:
                            state.policy = max_action
                            unchanged = False

            if unchanged:
                break

        return self.maze_grid
        # policy = []
        # for c in range(cols):
        #     policy.append([])
        #     for r in range(rows):
        #         state = self.maze_grid[c][r]
        #         policy[c].append(state.policy)
        #
        # return policy

    def evaluate_policy(self):
        new_maze_grid = copy.deepcopy(self.maze_grid)
        cols = len(self.maze_grid)
        rows = len(self.maze_grid[0])

        for c in range(cols):
            for r in range(rows):
                state = self.maze_grid[c][r]
                new_state = new_maze_grid[c][r]
                # if c == 2 and r == 2:
                    # print(self.maze_grid[c][r].policy)

                if not state.adp_new:
                    if not self.maze_grid[c][r].terminal and not self.maze_grid[c][r].obstacle:
                        if state.policy == constants.UP:
                            new_state.util = state.reward + self.gamma * self.get_up_util(c, r)
                        elif state.policy == constants.DOWN:
                            new_state.util = state.reward + self.gamma * self.get_down_util(c, r)
                        elif state.policy == constants.LEFT:
                            new_state.util = state.reward + self.gamma * self.get_left_util(c, r)
                        elif state.policy == constants.RIGHT:
                            new_state.util = state.reward + self.gamma * self.get_right_util(c, r)
                        else:
                            pass    # state is either terminal or obstacle

        return new_maze_grid
        # self.maze_grid = copy.deepcopy(new_maze_grid)

    def calc_new_util(self, col, row):
        max_util, max_action = self.get_max_util(col, row)
        util = self.maze_grid[col][row].reward + self.gamma * max_util
        return util, max_action

    def get_max_util(self, col, row):
        up_util = self.get_up_util(col, row)
        down_util = self.get_down_util(col, row)
        left_util = self.get_left_util(col, row)
        right_util = self.get_right_util(col, row)

        util_list = [up_util, down_util, left_util, right_util]
        max_util = max(util_list)
        max_pos = util_list.index(max_util)
        return max_util, max_pos

    def get_up_util(self, col, row):
        state = self.maze_grid[col][row]
        up_col, up_row = self.get_up_state(col, row)
        l_col, l_row = self.get_left_state(col, row)
        r_col, r_row = self.get_right_state(col, row)

        transition_dict = state.transition_model['UP']
        up_prob = transition_dict['UP']
        l_prob = transition_dict['LEFT']
        r_prob = transition_dict['RIGHT']

        util = up_prob * self.maze_grid[up_col][up_row].util + l_prob * self.maze_grid[l_col][l_row].util + r_prob * self.maze_grid[r_col][r_row].util

        return util

    def get_down_util(self, col, row):
        state = self.maze_grid[col][row]
        d_col, d_row = self.get_down_state(col, row)
        l_col, l_row = self.get_left_state(col, row)
        r_col, r_row = self.get_right_state(col, row)

        transition_dict = state.transition_model['DOWN']
        down_prob = transition_dict['DOWN']
        l_prob = transition_dict['LEFT']
        r_prob = transition_dict['RIGHT']

        util = down_prob * self.maze_grid[d_col][d_row].util + l_prob * self.maze_grid[l_col][l_row].util + r_prob * self.maze_grid[r_col][r_row].util

        return util

    def get_left_util(self, col, row):
        state = self.maze_grid[col][row]
        l_col, l_row = self.get_left_state(col, row)
        up_col, up_row = self.get_up_state(col, row)
        d_col, d_row = self.get_down_state(col, row)

        transition_dict = state.transition_model['LEFT']
        l_prob = transition_dict['LEFT']
        up_prob = transition_dict['UP']
        down_prob = transition_dict['DOWN']

        util = l_prob * self.maze_grid[l_col][l_row].util + up_prob * self.maze_grid[up_col][up_row].util + down_prob * self.maze_grid[d_col][d_row].util

        return util

    def get_right_util(self, col, row):
        state = self.maze_grid[col][row]
        r_col, r_row = self.get_right_state(col, row)
        up_col, up_row = self.get_up_state(col, row)
        d_col, d_row = self.get_down_state(col, row)

        transition_dict = state.transition_model['RIGHT']
        r_prob = transition_dict['RIGHT']
        up_prob = transition_dict['UP']
        down_prob = transition_dict['DOWN']

        util = r_prob * self.maze_grid[r_col][r_row].util + up_prob * self.maze_grid[up_col][up_row].util + down_prob * self.maze_grid[d_col][d_row].util
        # if col == 2 and row == 2:
        #     print(r_prob, self.maze_grid[r_col][r_row].util, self.maze_grid[col][row].adp_state_action_state_dict)

        return util

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

    def display_results(self):
        cols = len(self.maze_grid)
        rows = len(self.maze_grid[0])

        print("Policy table calculated:")
        for c in range(cols):
            for r in range(rows):
                state = self.maze_grid[c][r]
                print("({}, {}): {}".format(c + 1, r + 1, constants.action_list[state.policy]))

        print()

        print("Utilities:")
        for c in range(cols):
            for r in range(rows):
                state = self.maze_grid[c][r]
                print("({}, {}): {}".format(c + 1, r + 1, state.util))

        print()
