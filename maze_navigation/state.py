import maze_navigation.constants as constants


class State:

    def __init__(self, reward, obstacle, terminal, col, row, policy=0, util=0):
        self.reward = reward
        self.obstacle = obstacle
        self.terminal = terminal
        self.col = col
        self.row = row
        self.due = (0, 0)

        if self.terminal:
            self.policy = constants.TERMINAL
            self.util = self.reward
        elif self.obstacle:
            self.policy = constants.OBSTACLE
            self.util = None
        else:
            self.policy = policy
            self.util = util
