import maze_navigation.constants as constants
import random
import copy


class ReinforcementLearning:

    def __init__(self, maze_grid, mdp_policy):
        self.maze_grid = copy.deepcopy(maze_grid)
        self.mdp_policy = copy.deepcopy(mdp_policy)

    def adp(self):
        cols = len(self.maze_grid)
        rows = len(self.maze_grid[0])

        for c in range(cols):
            for r in range(rows):
                state = self.maze_grid[c][r]
                state.adp_state_action_state_dict = constants.blank_transition_model
                state.adp_state_action_dict = constants.blank_state_action_dict

        EPOCHS = 20000
        for i in range(EPOCHS):
            path = self.run_trial()
            self.update_adp_elements(path)

        for c in range(cols):
            for r in range(rows):
                state = self.maze_grid[c][r]
                for state_action_key in state.adp_state_action_dict:
                    state_action_count = state.adp_state_action_dict[state_action_key]
                    if state_action_count > 0:
                        for state_action_state_key in state.adp_state_action_state_dict[state_action_key]:
                            state_action_state_count = state.adp_state_action_state_dict[state_action_key][state_action_state_key]
                            state.transition_model[state_action_key][state_action_state_key] = state_action_state_count / state_action_count

        return self.maze_grid

    def update_adp_elements(self, path):
        for state in path:
            if not state.terminal:
                policy_action = self.mdp_policy[state.col][state.row]
                policy_action_key = str(constants.action_list[policy_action])
                actual_action_key = str(constants.action_list[state.action])

                state.adp_state_action_dict[policy_action_key] += 1

                state.adp_state_action_state_dict[policy_action_key][actual_action_key] += 1

    def due(self):
        EPOCHS = 100000
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
            action = self.mdp_policy[col][row]
            col, row, action = self.simulate_move(col, row, action)
            state.action = action
            path.append(state)
            state = self.maze_grid[col][row]
            # path.append(state)

        state.action = constants.TERMINAL
        path.append(state)

        return path

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
