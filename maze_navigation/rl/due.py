from maze_navigation.rl.rl import ReinforcementLearning
import maze_navigation.constants as constants


class Due(ReinforcementLearning):

    def due(self):
        EPOCHS = 1000
        cols = len(self.maze_grid)
        rows = len(self.maze_grid[0])

        for i in range(EPOCHS):
            path = self.run_trial()
            self.update_due_util(path)

        # for c in range(cols):
        #     for r in range(rows):
        #         state = self.maze_grid[c][r]
        #         print("({}, {}): {}".format(state.col + 1, state.row + 1, state.due[0]))
        # print()

        self.update_policy()
        return self.maze_grid

    def update_due_util(self, path):
        reverse_path = path
        reverse_path.reverse()
        reward_to_go = reverse_path[0].reward
        length = len(reverse_path)

        for i in range(length):
            state = reverse_path[i]
            due_util = state.due[0]
            count = state.due[1]

            new_due_util = (due_util * count + reward_to_go) / (count + 1)
            count += 1
            state.due = (new_due_util, count)

            if i < length - 1:
                next_state = reverse_path[i + 1]
                reward_to_go = reward_to_go + next_state.reward

    def run_trial(self):
        col, row = self.get_init_pos()
        state = self.maze_grid[col][row]
        path = []

        while not state.terminal:
            action = self.maze_grid[col][row].policy
            col, row, action = self.simulate_move(col, row, action)
            state.action = action
            path.append(state)
            state = self.maze_grid[col][row]
            # path.append(state)

        state.action = constants.TERMINAL
        path.append(state)

        return path

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

        util = self.maze_grid[up_col][up_row].due[0]

        return util

    def get_down_util(self, col, row):
        down_col, down_row = self.get_down_state(col, row)

        util = self.maze_grid[down_col][down_row].due[0]

        return util

    def get_left_util(self, col, row):
        l_col, l_row = self.get_left_state(col, row)

        util = self.maze_grid[l_col][l_row].due[0]

        return util

    def get_right_util(self, col, row):
        r_col, r_row = self.get_right_state(col, row)

        util = self.maze_grid[r_col][r_row].due[0]

        return util
