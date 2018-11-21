from maze_navigation.maze import Maze
from maze_navigation.mdp import Mdp
from maze_navigation.rl import ReinforcementLearning
# from maze_navigation.constants import default_transition_model


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


mazes = init_mazes()

mdp = Mdp(mazes['a'].grid)
mdp.init_policy()
mdp.init_util()
mdp_maze_grid = mdp.policy_iteration()
mdp.display_results()

rl = ReinforcementLearning(mdp_maze_grid)
rl.due()

rl = ReinforcementLearning(mdp_maze_grid)
rl.adp()

rl = ReinforcementLearning(mdp_maze_grid)
rl = rl.td()

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
