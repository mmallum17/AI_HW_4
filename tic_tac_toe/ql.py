import copy
import random
from tic_tac_toe.constants import player_dict


class QLearning:
    gamma = 0.9

    def __init__(self, state_space):
        self.states = copy.deepcopy(state_space)

    def ql(self):
        EPOCHS = 100000
        for i in range(EPOCHS):
            print('\n\n\n\n')
            print(f'Trial: {i}')
            epsilon = get_epsilon(i)

            self.run_trial(i, epsilon)

    def run_trial(self, i, epsilon):
        learning_rate = 1 / (i + 1)

        board, move = self.get_start_state()

        while not board.terminal:
            # print(player_dict[move])
            board.display()
            print()
            action = self.get_action(board, move, epsilon)
            action_board = action[0]
            q_val = action[1]

            opposing_player = get_opposing_player(move)
            # if opposing_player == player_dict['X']:
            #     print("X")
            #     print(action_board.x_q)
            #     action_board.display()
            # else:
            #     print("O")
            #     print(action_board.o_q)
            #     action_board.display()
            max_q_new_state = action_board.get_max_action(opposing_player, False)[1]

            q_val = q_val + learning_rate * (action[0].x_reward + self.gamma * max_q_new_state - q_val)
            board.add_action(action_board, move, q=q_val)

            board = action_board
            move = opposing_player

        board.display()

        # print()
        # action[0].display()
        # print(action[1])
        # actions = board.get_actions(move)
        # for action in actions:
        #     print(action[0].state)
        # print(player_dict[move])
        # print("\n\n")

    def get_action(self, board, move, epsilon):
        prob = random.uniform(0, 1)
        if prob > epsilon:
            action = board.get_max_action(move, True)
        else:
            action = board.get_random_action(move, True)

        return action

    def get_start_state(self):
        valid = False
        start_state = None

        while not valid:
            valid = True
            state_key = random.choice(list(self.states.keys()))
            start_state = self.states[state_key]
            if start_state.terminal:
                valid = False

        if start_state.move == player_dict['EMPTY']:
            start_move = str(random.randint(1, 2))
        else:
            start_move = start_state.move

        return start_state, start_move


def get_epsilon(i):
    if i <= 99900:
        epsilon = 1
    else:
        epsilon = 0.00000000000000000000000000000000000000000001
    # if i <= 75000:
    #     epsilon = float(1) - float(i / 83333)
    # elif i <= 99000:
    #     epsilon = 0.1
    # else:
    #     epsilon = 0.000000000000000000000000000001
    return epsilon


def get_opposing_player(player):
    if player == player_dict['X']:
        return player_dict['O']
    else:
        return player_dict['X']
