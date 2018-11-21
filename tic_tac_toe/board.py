from tic_tac_toe.constants import win_pos
from tic_tac_toe.constants import player_dict


class Board:

    def __init__(self, state):
        self.state = state
        self.x_reward = 0
        self.q = 0
        self.terminal = False
        self.move = player_dict['EMPTY']

        self.init_rewards()
        self.init_terminal()
        self.init_move()

    def init_rewards(self):
        x_player = player_dict['X']
        o_player = player_dict['O']

        for w in win_pos:
            if self.state[w[0]] == x_player and self.state[w[1]] == x_player and self.state[w[2]] == x_player:
                self.x_reward = 10

            if self.state[w[0]] == o_player and self.state[w[1]] == o_player and self.state[w[2]] == o_player:
                self.x_reward = -10

    def init_terminal(self):
        x_player = player_dict['X']
        o_player = player_dict['O']

        terminal = True
        for pos in self.state:
            if pos == 0:
                terminal = False

        for w in win_pos:
            if (self.state[w[0]] == x_player and self.state[w[1]] == x_player and self.state[w[2]] == x_player) or \
                    self.state[w[0]] == o_player and self.state[w[1]] == o_player and self.state[w[2]] == o_player:
                terminal = True

        self.terminal = terminal

    def init_move(self):
        x_player = player_dict['X']
        o_player = player_dict['O']

        x_count = 0
        o_count = 0

        for pos in self.state:
            if pos == x_player:
                x_count += 1
            elif pos == o_player:
                o_count += 1

        if x_count > o_count:
            self.move = o_player
        elif o_count > x_count:
            self.move = x_player
        else:
            self.move = player_dict['EMPTY']
