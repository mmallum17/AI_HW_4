from maze_navigation.rl.rl import ReinforcementLearning


class Td(ReinforcementLearning):

    def td(self):
        cols = len(self.maze_grid)
        rows = len(self.maze_grid[0])

        EPOCHS = 20000
        for i in range(EPOCHS):
            self.run_td_trial(i)

        for c in range(cols):
            for r in range(rows):
                state = self.maze_grid[c][r]
                print("({}, {}): {}".format(state.col + 1, state.row + 1, state.util))
        print()

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
