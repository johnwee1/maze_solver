import csv
import copy
import numpy as np
import cv2

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
maze_wall = 0
maze_path = 1


def exportMaze(filename):
    maze = []
    gems = []
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
    return np.array(maze, dtype=np.int8), start_coord, end_coord


def create_monochrome_image(array, scale=1):
    # Ensure the array contains only 0s and 1s
    assert np.array_equal(
        array, array.astype(bool)
    ), "Array values must be either 0 or 1"

    # Convert the array to a uint8 type
    image_data = array.astype(np.uint8) * 255

    # Reshape the array to a 2D image
    image = np.reshape(image_data, (array.shape[0], array.shape[1]))

    # Scale the image based on the provided scale factor
    scaled_image = cv2.resize(
        image, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST
    )

    # Create a monochrome image using OpenCV
    monochrome_image = cv2.merge([scaled_image, scaled_image, scaled_image])

    return monochrome_image

if __name__=="__main__":
    # Example usage:
    maze, st, e = exportMaze("finalmaze.csv")
    print(maze)
    np_maze = np.array(maze, dtype=np.int8)

    result_image = create_monochrome_image(np_maze, scale=12)
    # cv2.imshow("Monochrome Image", result_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
