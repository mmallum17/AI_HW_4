from tic_tac_toe.constants import win_pos
from tic_tac_toe.constants import player_dict
from tic_tac_toe.constants import board_size
import random


class Board:

    def __init__(self, state):
        self.state = state
        self.x_reward = 0
        self.o_reward = 0
        self.terminal = False
        self.move = player_dict['EMPTY']
        self.x_q = []
        self.o_q = []
        self.x_count = 0
        self.o_count = 0

        self.init_rewards()
        self.init_terminal()
        self.init_move_and_count()

    def init_rewards(self):
        x_player = player_dict['X']
        o_player = player_dict['O']

        for w in win_pos:
            if self.state[w[0]] == x_player and self.state[w[1]] == x_player and self.state[w[2]] == x_player:
                self.x_reward = 10
                self.o_reward = -10

            if self.state[w[0]] == o_player and self.state[w[1]] == o_player and self.state[w[2]] == o_player:
                self.x_reward = -10
                self.o_reward = 10

    def init_terminal(self):
        x_player = player_dict['X']
        o_player = player_dict['O']

        terminal = True
        for pos in self.state:
            if pos == player_dict['EMPTY']:
                terminal = False

        for w in win_pos:
            if (self.state[w[0]] == x_player and self.state[w[1]] == x_player and self.state[w[2]] == x_player) or \
                    self.state[w[0]] == o_player and self.state[w[1]] == o_player and self.state[w[2]] == o_player:
                terminal = True

        self.terminal = terminal

    def init_move_and_count(self):
        x_player = player_dict['X']
        o_player = player_dict['O']

        x_count = 0
        o_count = 0

        for pos in self.state:
            if pos == x_player:
                x_count += 1
            elif pos == o_player:
                o_count += 1

        self.x_count = x_count
        self.o_count = o_count

        if self.terminal:
            self.move = player_dict['EMPTY']
        elif x_count > o_count:
            self.move = o_player
        elif o_count > x_count:
            self.move = x_player
        else:
            self.move = player_dict['EMPTY']

    def compare(self, temp_board, player):
        self_list = []
        temp_list = []

        for i in range(board_size):
            if self.state[i] == player:
                self_list.append(i)
            if temp_board[i] == player:
                temp_list.append(i)

        # print(self_list)
        # print(temp_list)
        dif = set(self_list).symmetric_difference(temp_list)
        return len(dif)

    def add_action(self, board, player, q=0):
        # print(board)
        # print("ADDED BACK")
        if player_dict['X'] == player:
            self.x_q.append((board, q))
        else:
            self.o_q.append((board, q))

    def get_max_action(self, player, remove):
        if self.terminal:
            return None, self.x_reward
        else:
            actions = self.get_actions(player)
            # max_action = None
            # max_index = 0
            # max_value = actions[0][1]
            #
            # for i in range(len(actions)):
            #     action = actions[i]
            #     q_val = action[1]
            #     if q_val > max_value:
            #         max_value = q_val
            #         max_index = i
            # if len(actions) == 1:
            #     max_action = actions[0]
            # else:
            max_action = max(actions, key=lambda item:item[1])
            # print(actions)
            if remove:
                actions.remove(max_action)

        return max_action

    def get_random_action(self, player, remove):
        actions = self.get_actions(player)

        random_action = random.choice(actions)
        if remove:
            actions.remove(random_action)

        return random_action

    def get_actions(self, player):
        if player_dict['X'] == player:
            return self.x_q
        else:
            return self.o_q

    def display(self):
        for i in range(3):
            index = 2 - i
            for j in range(3):
                player = player_dict[self.state[index * 3 + j]]
                if j == 0 or j == 1:
                    print(f' {player} |', end='')
                else:
                    print(f' {player}', end='')

            print()
            if index == 2 or index == 1:
                print('-----------')
