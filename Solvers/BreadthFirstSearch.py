"""
Source code taken from:
How to Solve a Maze using BFS in Python by Timur Bakibayev:
https://levelup.gitconnected.com/solve-a-maze-with-python-e9f0580979a1
"""

from PIL import Image, ImageDraw  # install Pillow package to use PIL

images = []
# this list of images will be animated together to form the final .gif output
# default BFS maze
a = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

zoom = 20
borders = 8
start = 1, 1  # define start point at (1, 1)
end = 2, 5  # define end point at (2, 5)

"""
your maze --- TO CHANGE FOR YOUR MAZE DESIGN ---
"""
# your maze --- TO REFER FOR YOUR MAZE DESIGN ---
# a = [
#     [1, 1, 1, 1, 1, 1, 1],
#     [1, 0, 0, 1, 0, 0, 1],
#     [1, 0, 0, 0, 0, 0, 1],
#     [1, 0, 0, 0, 1, 0, 1],
#     [1, 1, 1, 0, 1, 1, 1],
#     [1, 0, 0, 0, 0, 0, 1],
#     [1, 1, 1, 1, 1, 1, 1]
# ]
#
# zoom = 20
# borders = 6
# start = 1, 5  # define start point at (1, 5)
# end = 4, 3    # define end point at (4, 3)

"""
DO NOT NEED TO CHANGE THIS SECTION --- START
"""


def make_step(k):
    """m is a copy of matrix a
    k is the current step count

    `make_step` advancess the boundary (see the gif) of the search space (by checking if m[i][j]=k) and assigns value k+1 to a box just outside the space

    skips the box if visited (because otherwise the path automatically gets cut off and it'd be a cycle anyways.)
    """
    for i in range(len(m)):  # number of rows
        for j in range(len(m[i])):  # number of cols
            if m[i][j] == k:  # if the position matches the value of k
                if i > 0 and m[i - 1][j] == 0 and a[i - 1][j] == 0:  # if box down is 0
                    m[i - 1][j] = k + 1
                if (
                    j > 0 and m[i][j - 1] == 0 and a[i][j - 1] == 0
                ):  # if box to the left is 0
                    m[i][j - 1] = k + 1
                if (
                    i < len(m) - 1 and m[i + 1][j] == 0 and a[i + 1][j] == 0
                ):  # if box up is 0
                    m[i + 1][j] = k + 1
                if (
                    j < len(m[i]) - 1 and m[i][j + 1] == 0 and a[i][j + 1] == 0
                ):  # if box right is 0
                    m[i][j + 1] = k + 1


def print_m(m):
    """Helper function to print the maze."""
    for i in range(len(m)):
        for j in range(len(m[i])):
            print(str(m[i][j]).ljust(2), end=" ")
        print()


def draw_matrix(a, m, the_path=[]):
    """helper function that takes in the original matrix a and the copy of the matrix m, along with an optional path list.
    uses the opencv library that you can install via `pip install opencv-python` in your terminal
    """

    im = Image.new(
        "RGB", (zoom * len(a[0]), zoom * len(a)), (255, 255, 255)
    )  # Creates a new image of reasonable resolution
    draw = ImageDraw.Draw(im)  # init draw obj
    for i in range(len(a)):
        for j in range(len(a[i])):
            color = (255, 255, 255)  # white
            r = 0
            if a[i][j] == 1:  # if the current pixel is 0, color = black
                color = (0, 0, 0)
            if i == start[0] and j == start[1]:  # if location is at start
                color = (0, 255, 0)
                r = borders
            if i == end[0] and j == end[1]:  # if location is at end draw
                color = (0, 255, 0)
                r = borders
            draw.rectangle(
                (
                    j * zoom + r,
                    i * zoom + r,
                    j * zoom + zoom - r - 1,
                    i * zoom + zoom - r - 1,
                ),
                fill=color,
            )
            if m[i][j] > 0:
                r = borders
                draw.ellipse(
                    (
                        j * zoom + r,
                        i * zoom + r,
                        j * zoom + zoom - r - 1,
                        i * zoom + zoom - r - 1,
                    ),
                    fill=(255, 0, 0),
                )
    for u in range(len(the_path) - 1):
        """Block of code draws lines that links the grid together."""
        y = the_path[u][0] * zoom + int(zoom / 2)
        x = the_path[u][1] * zoom + int(zoom / 2)
        y1 = the_path[u + 1][0] * zoom + int(zoom / 2)
        x1 = the_path[u + 1][1] * zoom + int(zoom / 2)
        draw.line((x, y, x1, y1), fill=(255, 0, 0), width=5)
    draw.rectangle(
        (0, 0, zoom * len(a[0]), zoom * len(a)), outline=(0, 255, 0), width=2
    )
    images.append(im)


# block of code makes the matrix
m = []
for i in range(len(a)):
    m.append([])
    for j in range(len(a[i])):
        m[-1].append(0)
i, j = start  # sets the start point
m[i][j] = 1

k = 0
while m[end[0]][end[1]] == 0:
    """while the end position has not been reached, and is still empty (hence 0)
    increment k to feed into make_step"""
    k += 1
    make_step(k)
    draw_matrix(a, m)  # generates a frame for every step of the search iteration

i, j = end
k = m[i][j]
the_path = [(i, j)]
while k > 1:
    if i > 0 and m[i - 1][j] == k - 1:
        i, j = i - 1, j
        the_path.append((i, j))
        k -= 1
    elif j > 0 and m[i][j - 1] == k - 1:
        i, j = i, j - 1
        the_path.append((i, j))
        k -= 1
    elif i < len(m) - 1 and m[i + 1][j] == k - 1:
        i, j = i + 1, j
        the_path.append((i, j))
        k -= 1
    elif j < len(m[i]) - 1 and m[i][j + 1] == k - 1:
        i, j = i, j + 1
        the_path.append((i, j))
        k -= 1
    draw_matrix(a, m, the_path)

for i in range(10):
    # draw the blinking at the end
    if i % 2 == 0:
        draw_matrix(a, m, the_path)
    else:
        draw_matrix(a, m)

"""
DO NOT NEED TO CHANGE THIS SECTION --- END
"""

print_m(m)
print(the_path)

# default BFS maze
images[0].save(
    "default_bfs_sol_2.gif",  # change the location because backslash pathing only works on windows
    save_all=True,
    append_images=images[1:],
    optimize=False,
    duration=1,
    loop=0,
)

"""
your maze --- TO CHANGE FOR YOUR MAZE DESIGN ---
"""
# images[0].save('maze_sols\maze_bfs_sol.gif', save_all=True, append_images=images[1:], optimize=False, duration=1,
#                loop=0)
