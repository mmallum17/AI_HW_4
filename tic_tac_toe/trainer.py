from tic_tac_toe.board import Board
from tic_tac_toe.constants import board_size
from tic_tac_toe.constants import player_dict
from tic_tac_toe.constants import win_pos


def init_board_states():
    state = ['0'] * board_size
    for i in range(3):
        state[0] = str(i)
        for j in range(3):
            state[1] = str(j)
            for k in range(3):
                state[2] = str(k)
                for l in range(3):
                    state[3] = str(l)
                    for m in range(3):
                        state[4] = str(m)
                        for n in range(3):
                            state[5] = str(n)
                            for o in range(3):
                                state[6] = str(o)
                                for p in range(3):
                                    state[7] = str(p)
                                    for q in range(3):
                                        state[8] = str(q)
                                        if valid_state(state):
                                            state_str = "".join(state)
                                            states[state_str] = Board(state)


def valid_state(state):
    valid = True
    x_player = player_dict['X']
    o_player = player_dict['O']

    x_count = 0
    o_count = 0

    for pos in state:
        if pos == x_player:
            x_count += 1
        elif pos == o_player:
            o_count += 1

    if abs(x_count - o_count > 1):
        valid = False

    for w in win_pos:
        if (state[w[0]] == x_player and state[w[1]] == x_player and state[w[2]] == x_player) and \
                state[w[0]] == o_player and state[w[1]] == o_player and state[w[2]] == o_player:
            valid = False

    return valid


states = {}
init_board_states()
print(len(states))
