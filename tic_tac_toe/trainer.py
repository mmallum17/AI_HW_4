from tic_tac_toe.board import Board
from tic_tac_toe.constants import board_size
from tic_tac_toe.constants import player_dict
from tic_tac_toe.constants import win_pos
from tic_tac_toe.ql import QLearning
import random
import copy
import csv


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
                                            states[state_str] = Board(copy.deepcopy(state))

    set_board_actions()


def set_board_actions():
    i = 0
    for key in states:
        # if i == 10:
        #     break
        print(i)
        i += 1
        board = states[key]

        if not board.terminal:
            if board.move == player_dict['X'] or board.move == player_dict['EMPTY']:
                add_x_actions(board)
            if board.move == player_dict['O'] or board.move == player_dict['EMPTY']:
                add_o_actions(board)


def add_x_actions(board):
    for key in states:
        temp_board = states[key]
        if board.compare(temp_board.state, player_dict['X']) == 1 and \
                board.compare(temp_board.state, player_dict['O']) == 0 and board.x_count == temp_board.x_count - 1:
            board.add_action(temp_board, player_dict['X'])


def add_o_actions(board):
    for key in states:
        temp_board = states[key]
        if board.compare(temp_board.state, player_dict['O']) == 1 and \
                board.compare(temp_board.state, player_dict['X']) == 0 and board.o_count == temp_board.o_count - 1:
            board.add_action(temp_board, player_dict['O'])


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

    if abs(x_count - o_count) > 1:
        valid = False

    o_wins = False
    x_wins = False
    for w in win_pos:
        if state[w[0]] == x_player and state[w[1]] == x_player and state[w[2]] == x_player:
            x_wins = True
        if state[w[0]] == o_player and state[w[1]] == o_player and state[w[2]] == o_player:
            o_wins = True

    if x_wins and o_wins:
        valid = False

    return valid


def save_boards_to_csv():
    with open('tic_tac_toe_x_actions.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')

        for key in states:
            temp_list = [key]
            state = states[key]
            for action_board in state.x_q:
                board_str = "".join(action_board[0].state)
                temp_list.append(board_str)
            csv_writer.writerow(temp_list)

    with open('tic_tac_toe_o_actions.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')

        for key in states:
            temp_list = [key]
            state = states[key]
            for action_board in state.o_q:
                board_str = "".join(action_board[0].state)
                temp_list.append(board_str)
            csv_writer.writerow(temp_list)


def read_board_states():
    with open('tic_tac_toe_x_actions.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            board = row[0]
            states[board] = Board(list(board))

    with open('tic_tac_toe_x_actions.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            board = row[0]
            row_length = len(row)
            for i in range(1, row_length):
                action = states[row[i]]
                states[board].add_action(action, player_dict['X'])

    with open('tic_tac_toe_o_actions.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            board = row[0]
            row_length = len(row)
            for i in range(1, row_length):
                action = states[row[i]]
                states[board].add_action(action, player_dict['O'])


states = {}
# init_board_states()
# save_boards_to_csv()
read_board_states()
# print(states['202100121'].o_q)
ql = QLearning(states)
ql.ql()


# choice_one = random.choice(list(states.keys()))
# choice_two = random.choice(list(states.keys()))
# print(len(states))
# print(states[choice_one].compare(states[choice_one].state, player_dict['EMPTY']))
# print(choice_one)
# state = states[choice_one]
# state.display()
# for action in states[choice_one].x_q:
#     print(action[0].state)
# print(states[choice_one].state)
# print(states[choice_two].state)
