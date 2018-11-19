import random
import copy

gamma = 0.9


def evaluate_policy(utility_grid, policy_list):
    new_grid = copy.deepcopy(utility_grid)

    for state in range(len(utility_grid) - 1):
        if policy_list[state] == 0:
            new_grid[state] = reward[state] + gamma * get_up_util(state, utility_grid)
        elif policy_list[state] == 1:
            new_grid[state] = reward[state] + gamma * get_down_util(state, utility_grid)
        elif policy_list[state] == 2:
            new_grid[state] = reward[state] + gamma * get_left_util(state, utility_grid)
        else:
            new_grid[state] = reward[state] + gamma + get_right_util(state, utility_grid)

    return new_grid


def init_policy_vector():
    policy_list = []
    for i in range(len(reward) - 1):
        policy_list.append(random.randint(0, 3))
    policy_list.append(4)
    return policy_list


def policy_iteration(utility_grid):
    policy_list = init_policy_vector()
    while True:
        utility_grid = evaluate_policy(utility_grid, policy_list)
        unchanged = True

        for state in range(len(utility_grid) - 1):
            new_utility, max_pos = calc_new_utility(state, utility_grid)
            if new_utility > utility_grid[state]:
                policy_list[state] = max_pos
                unchanged = False

        if unchanged:
            break

    display_results(utility_grid, policy_list)


def calc_new_utility(state, utility_grid):
    max_util, max_pos = get_max_utility(state, utility_grid)
    utility = reward[state] + gamma * max_util
    return utility, max_pos


def get_max_utility(state, utility_grid):
    up_util = get_up_util(state, utility_grid)
    down_util = get_down_util(state, utility_grid)
    left_util = get_left_util(state, utility_grid)
    right_util = get_right_util(state, utility_grid)

    util_list = [up_util, down_util, left_util, right_util]
    max_util = max(util_list)
    max_pos = util_list.index(max_util)
    return max_util, max_pos


def get_up_util(state, utility_grid):
    up_state = get_up_state(state)
    left_state = get_left_state(state)
    right_state = get_right_state(state)

    util = 0.8 * utility_grid[up_state] + 0.1 * utility_grid[left_state] + 0.1 * utility_grid[right_state]
    return util


def get_down_util(state, utility_grid):
    down_state = get_down_state(state)
    left_state = get_left_state(state)
    right_state = get_right_state(state)

    util = 0.8 * utility_grid[down_state] + 0.1 * utility_grid[left_state] + 0.1 * utility_grid[right_state]
    return util


def get_left_util(state, utility_grid):
    left_state = get_left_state(state)
    up_state = get_up_state(state)
    down_state = get_down_state(state)

    util = 0.8 * utility_grid[left_state] + 0.1 * utility_grid[up_state] + 0.1 * utility_grid[down_state]
    return util


def get_right_util(state, utility_grid):
    right_state = get_right_state(state)
    up_state = get_up_state(state)
    down_state = get_down_state(state)

    util = 0.8 * utility_grid[right_state] + 0.1 * utility_grid[up_state] + 0.1 * utility_grid[down_state]
    return util


def get_up_state(state):
    # Get location if going up
    if state >= 6:
        up_state = state
    else:
        up_state = state + 3
    return up_state


def get_down_state(state):
    # Get location if going down
    if state <= 2:
        down_state = state
    else:
        down_state = state - 3
    return down_state


def get_left_state(state):
    # Get location if going left
    if state % 3 == 0:
        left_state = state
    else:
        left_state = state - 1
    return left_state


def get_right_state(state):
    # Get location if going right
    if state % 3 == 2:
        right_state = state
    else:
        right_state = state + 1
    return right_state
