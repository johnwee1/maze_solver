import csv
from functionizedbfs import Solver

# CSV LEGEND
PATH = ""  # maps to a maze_path
GEM = "G"  # maps to a maze_path
START, END = "S", "E"  # maps to a maze_path
MONSTER = "M"  # maps to a maze_path because monsters cannot be represented
HEARTS = 'H'
maze_paths = {PATH, GEM, START, END, MONSTER, HEARTS}
WALL = "#"  # maps to a maze_wall
RIVER = "R"  # maps to a maze_wall
maze_walls = {WALL, RIVER}

# BFS SOLVER LEGEND
maze_wall = 1
maze_path = 0

gems = []

def exportMaze(filename):
    maze = []
    start_coord = None
    end_coord = None
    with open(filename, newline="") as f:
        csvlines = csv.reader(f, delimiter=",")
        for row_num, row in enumerate(csvlines):
            res = []
            for col_num, char in enumerate(row):
                char = char.upper()
                if char in maze_paths:
                    if char == START:
                        start_coord = row_num, col_num
                    if char == END:
                        end_coord = row_num, col_num
                    if char == GEM:
                        gems.append((row_num, col_num))
                    res.append(maze_path)
                else:
                    res.append(maze_wall)
            maze.append(res)
    return maze, start_coord, end_coord

# Example usage:
maze, start, end = exportMaze("finalmaze.csv")

solver = Solver(maze,start,gems,end)
solver.solve_maze()
images = solver.images
images[0].save(
        "solution_with_gems.gif",  # change the location because backslash pathing only works on windows
        save_all=True,
        append_images=images[1:],
        optimize=False,
        duration=1,
        loop=0,
    )

solver_wo_gems = Solver(maze, start, [], end)
solver_wo_gems.solve_maze()
images = solver_wo_gems.images
images[0].save(
        "solution_no_gems.gif",  # change the location because backslash pathing only works on windows
        save_all=True,
        append_images=images[1:],
        optimize=False,
        duration=1,
        loop=0,
    )