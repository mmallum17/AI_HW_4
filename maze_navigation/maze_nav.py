from maze_navigation.models.maze import Maze
from maze_navigation.mdp import Mdp
from maze_navigation.rl.adp import Adp
from maze_navigation.rl.due import Due
from maze_navigation.rl.td import Td
import maze_navigation.constants as constants
import random


def init_mazes():
    mazes = {}

    # Add first maze
    maze = Maze(4, 3)
    maze.set_obstacles([(2, 2)])
    maze.set_rewards([(4, 3, 1), (4, 2, -1)])
    maze.set_terminal([(4, 3), (4, 2)])
    mazes['a'] = maze

    # Add second maze
    maze = Maze(10, 10)
    maze.set_rewards([(5, 5, 1)])
    maze.set_terminal([(5, 5)])
    mazes['b'] = maze

    # Add third maze
    maze = Maze(10, 10)
    maze.set_obstacles([(4, 4), (6, 4), (4, 6), (6, 6)])
    maze.set_rewards([(5, 5, 1)])
    maze.set_terminal([(5, 5)])
    mazes['c'] = maze

    # Add fourth maze
    maze = Maze(10, 10)
    maze.set_obstacles([(4, 4), (6, 4), (4, 6), (6, 6)])
    maze.set_rewards([(5, 5, 1), (5, 7, -1), (4, 5, -1)])
    maze.set_terminal([(5, 5), (5, 7), (4, 5)])
    mazes['d'] = maze

    return mazes


def select_maze(mazes):
    valid = False
    maze_choice = None

    while not valid:
        valid = True
        maze_choice = input('Select a maze by entering a, b, c, or d or enter e to exit: ')
        if maze_choice not in mazes.keys() and maze_choice != 'e':
            valid = False

    return maze_choice


def select_algorithm():
    valid = False
    algorithm_choice = None

    while not valid:
        valid = True
        algorithm_choice = input('Enter 1, 2, or 3 to select an algorithm (1. DUE, 2. ADP, 3. TD): ')
        if algorithm_choice != '1' and algorithm_choice != '2' and algorithm_choice != '3':
            valid = False

    return algorithm_choice


def get_start_coordinates(maze):
    valid = False
    cols = len(maze.grid)
    rows = len(maze.grid[0])
    col = None
    row = None

    while not valid:
        valid = True
        try:
            print("The bottom left location is (1,1)!")
            coordinates = input("Please enter start coordinates in the following format <col> <row> (Example: '1 1'): ")
            coordinates = coordinates.split(' ')
            col = int(coordinates[0]) - 1
            row = int(coordinates[1]) - 1
            if col >= cols or row >= rows:
                valid = False
            if maze.grid[col][row].obstacle:
                valid = False
        except:
            valid = False

    return col, row


def follow_policy(trained_grid, coordinates):
    col = coordinates[0]
    row = coordinates[1]
    state = trained_grid[col][row]
    path = [(col, row)]

    while not state.terminal:
        if state.policy == constants.UP:
            col, row = move_up(col, row, trained_grid)
        elif state.policy == constants.DOWN:
            col, row = move_down(col, row, trained_grid)
        elif state.policy == constants.LEFT:
            col, row = move_left(col, row, trained_grid)
        else:
            col, row = move_right(col, row, trained_grid)
        state = trained_grid[col][row]
        path.append((col, row))

    return path


def move_up(col, row, trained_grid):
    option = random.randint(0, 9)
    if option <= 7:
        new_state = get_up_state(col, row, trained_grid)
    elif option == 8:
        new_state = get_left_state(col, row, trained_grid)
    else:
        new_state = get_right_state(col, row, trained_grid)
    return new_state


def move_down(col, row, trained_grid):
    option = random.randint(0, 9)
    if option <= 7:
        new_state = get_down_state(col, row, trained_grid)
    elif option == 8:
        new_state = get_left_state(col, row, trained_grid)
    else:
        new_state = get_right_state(col, row, trained_grid)
    return new_state


def move_left(col, row, trained_grid):
    option = random.randint(0, 9)
    if option <= 7:
        new_state = get_left_state(col, row, trained_grid)
    elif option == 8:
        new_state = get_up_state(col, row, trained_grid)
    else:
        new_state = get_down_state(col, row, trained_grid)
    return new_state


def move_right(col, row, trained_grid):
    option = random.randint(0, 9)
    if option <= 7:
        new_state = get_right_state(col, row, trained_grid)
    elif option == 8:
        new_state = get_up_state(col, row, trained_grid)
    else:
        new_state = get_down_state(col, row, trained_grid)
    return new_state


def get_up_state(col, row, trained_grid):
    row_size = len(trained_grid[0])

    # Get location if going up
    if row >= row_size - 1 or trained_grid[col][row + 1].obstacle:
        up_state = col, row
    else:
        up_state = col, row + 1
    return up_state


def get_down_state(col, row, trained_grid):
    # Get location if going down
    if row <= 0 or trained_grid[col][row - 1].obstacle:
        down_state = col, row
    else:
        down_state = col, row - 1
    return down_state


def get_left_state(col, row, trained_grid):
    # Get location if going left
    if col <= 0 or trained_grid[col - 1][row].obstacle:
        left_state = col, row
    else:
        left_state = col - 1, row
    return left_state


def get_right_state(col, row, trained_grid):
    col_size = len(trained_grid)

    # Get location if going right
    if col >= col_size - 1 or trained_grid[col + 1][row].obstacle:
        right_state = col, row
    else:
        right_state = col + 1, row
    return right_state


mazes = init_mazes()

while True:
    maze_choice = select_maze(mazes)
    if maze_choice == 'e':
        break
    maze = mazes[maze_choice]
    print()
    algorithm = select_algorithm()
    print()

    mdp = Mdp(maze.grid)
    mdp.init_policy()
    mdp.init_util()
    mdp_maze_grid = mdp.policy_iteration()
    trained_maze_grid = None

    if algorithm == '1':
        due = Due(mdp_maze_grid)
        trained_maze_grid = due.due()
    elif algorithm == '2':
        adp = Adp(mdp_maze_grid)
        trained_maze_grid = adp.adp()
    elif algorithm == '3':
        td = Td(mdp_maze_grid)
        trained_maze_grid = td.td()

    coordinates = get_start_coordinates(maze)
    path = follow_policy(trained_maze_grid, coordinates)
    print()
    print("Path taken, where the bottom left location is (1, 1)")
    for i in range(len(path)):
        state = path[i]
        print(f'Move {i}:     {state[0] + 1}, {state[1] + 1} ')
    print()
# rl = ReinforcementLearning(mazes['a'].grid, mdp_policy)
# adp_maze_grid = rl.adp()
# mdp = Mdp(adp_maze_grid)
# mdp_policy = mdp.policy_iteration()
# mdp.display_results()
# cols = len(mazes['a'].grid)
# rows = len(mazes['a'].grid[0])


# for c in range(len(mazes['a'].grid)):
#     for r in range(len(mazes['a'].grid[0])):
#         print(mazes['a'].grid[c][r].obstacle)
# mdp.policy_iteration()
# mdp.display_results()
# print(mazes['b'].grid[0][0].reward)

# maze = Maze(4, 3)
# print(len(maze.grid))
