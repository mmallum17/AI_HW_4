from maze_navigation.rl.rl import ReinforcementLearning
from maze_navigation.mdp import Mdp
import copy
import maze_navigation.constants as constants


class Adp(ReinforcementLearning):

    def adp(self):
        cols = len(self.maze_grid)
        rows = len(self.maze_grid[0])

        for c in range(cols):
            for r in range(rows):
                state = self.maze_grid[c][r]
                state.adp_state_action_state_dict = copy.deepcopy(constants.blank_transition_model)
                state.adp_state_action_dict = copy.deepcopy(constants.blank_state_action_dict)
                state.transition_model = copy.deepcopy(constants.blank_transition_model)
                state.adp_new = True

        EPOCHS = 100
        for i in range(EPOCHS):
            self.run_adp_trial()

        self.update_policy()
        # mdp = Mdp(self.maze_grid)
        # mdp.display_results()

        return self.maze_grid

    def update_policy(self):
        cols = len(self.maze_grid)
        rows = len(self.maze_grid[0])

        for c in range(cols):
            for r in range(rows):
                state = self.maze_grid[c][r]
                _, max_action = self.get_max_util(c, r)
                state.policy = max_action

    def run_adp_trial(self):
        # Get starting position
        col, row = self.get_init_pos()
        state = self.maze_grid[col][row]
        if state.adp_new:
            state.adp_new = False
            state.util = state.reward

        # Run trial to a terminal state
        while not state.terminal:
            # Get new state
            policy_action = self.maze_grid[col][row].policy
            col, row, action_taken = self.simulate_move(col, row, policy_action)
            new_state = self.maze_grid[col][row]

            # Update new state
            if new_state.adp_new:
                new_state.adp_new = False
                new_state.util = new_state.reward

            # Update old state
            policy_action_key = str(constants.action_list[policy_action])
            action_taken_key = str(constants.action_list[action_taken])
            s_a_dict = state.adp_state_action_dict
            s_a_s_dict = state.adp_state_action_state_dict
            s_a_dict[policy_action_key] += 1
            s_a_s_dict[policy_action_key][action_taken_key] += 1
            for action_key in s_a_s_dict[policy_action_key]:
                if s_a_s_dict[policy_action_key][action_key] > 0:
                    state.transition_model[policy_action_key][action_key] = s_a_s_dict[policy_action_key][action_key] / s_a_dict[policy_action_key]

            # Policy evaluation
            mdp = Mdp(self.maze_grid)
            new_maze_grid = mdp.evaluate_policy()
            self.maze_grid = copy.deepcopy(new_maze_grid)

            state = new_state

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

        return util
