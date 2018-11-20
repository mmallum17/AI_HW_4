from maze_navigation.state import State


class Maze:

    def __init__(self, cols, rows):
        self.grid = []
        for c in range(cols):
            self.grid.append([])
            for r in range(rows):
                self.grid[c].append(State(-0.04, False, False))

        # for c in range(cols):
        #     for r in range(rows):
        #         self.grid[c][r] = State(-0.04, False, False)

    def set_obstacles(self, obstacle_list):
        for o in obstacle_list:
            col = o[0] - 1
            row = o[1] - 1
            self.grid[col][row].obstacle = True

    def set_rewards(self, rewards_list):
        for r in rewards_list:
            col = r[0] - 1
            row = r[1] - 1
            reward = r[2]
            self.grid[col][row].reward = reward

    def set_terminal(self, terminal_list):
        for t in terminal_list:
            col = t[0] - 1
            row = t[1] - 1
            self.grid[col][row].terminal = True
