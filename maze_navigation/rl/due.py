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

        for c in range(cols):
            for r in range(rows):
                state = self.maze_grid[c][r]
                print("({}, {}): {}".format(state.col + 1, state.row + 1, state.due[0]))
        print()

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
