from maze_navigation.maze import Maze


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
# print(mazes['b'].grid[0][0].reward)

# maze = Maze(4, 3)
# print(len(maze.grid))
