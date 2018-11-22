from maze_navigation.rl.rl import ReinforcementLearning


class Td(ReinforcementLearning):

    def td(self):
        cols = len(self.maze_grid)
        rows = len(self.maze_grid[0])

        EPOCHS = 20000
        for i in range(EPOCHS):
            self.run_td_trial(i)

        self.update_policy()

        return self.maze_grid
        # for c in range(cols):
        #     for r in range(rows):
        #         state = self.maze_grid[c][r]
        #         print("({}, {}): {}".format(state.col + 1, state.row + 1, state.util))
        # print()

    def run_td_trial(self, i):
        col, row = self.get_init_pos()
        state = self.maze_grid[col][row]
        learning_rate = 1 / (i + 1)

        while not state.terminal:
            action = self.maze_grid[col][row].policy
            col, row, _ = self.simulate_move(col, row, action)
            new_state = self.maze_grid[col][row]
            state.util = state.util + learning_rate * (state.reward + new_state.util - state.util)
            state = new_state

    def update_policy(self):
        cols = len(self.maze_grid)
        rows = len(self.maze_grid[0])

        for c in range(cols):
            for r in range(rows):
                state = self.maze_grid[c][r]
                _, max_action = self.get_max_util(c, r)
                state.policy = max_action

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
        up_col, up_row = self.get_up_state(col, row)

        util = self.maze_grid[up_col][up_row].util

        return util

    def get_down_util(self, col, row):
        down_col, down_row = self.get_down_state(col, row)

        util = self.maze_grid[down_col][down_row].util

        return util

    def get_left_util(self, col, row):
        l_col, l_row = self.get_left_state(col, row)

        util = self.maze_grid[l_col][l_row].util

        return util

    def get_right_util(self, col, row):
        r_col, r_row = self.get_right_state(col, row)

        util = self.maze_grid[r_col][r_row].util

        return util
