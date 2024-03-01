"""
Source code modified from provided bfs
"""
from typing import List
import numpy as np
from PIL import Image, ImageDraw  # install Pillow package to use PIL


class Solver:
    def __init__(
        self, a: List[List[tuple]], start: tuple, vertices: List[tuple], end: tuple
    ) -> None:
        for v in vertices:
            if a[v[0]][v[1]] != 0:
                raise ValueError(f"Error: {v} is not an accessible square")
        if a[start[0]][start[1]] != 0:
            raise ValueError(f"Error: Start point {start} is not an accessible square")
        if a[end[0]][end[1]] != 0:
            raise ValueError(f"Error: End point {end} is not an accessible square")
        self.a = a
        self.m = np.zeros(
            np.shape(a), dtype=np.intc
        )  # turn into np array for easier indexing + faster.
        self.vertices = set(vertices)  # hash vertices for faster removal
        self.end = end
        self.current_path = []
        self.images = []
        self.start = start
        self.zoom = 20
        self.borders = 8

    def return_vertex_reached(self, m):
        """checks if any vertex has been reached (value set to some k)
        if no more vertices left return False"""
        if len(self.vertices) == 0:
            return False
        for v in self.vertices:
            if m[v] != 0:
                return v
        return None

    def solve_maze(self):
        self.__bfs(self.start)
        self.current_path.append(self.end)
        print(self.current_path)
        self.draw_matrix()
        # fix off by one error

    def draw_matrix(self):
        """helper function that takes in the original matrix a and the copy of the matrix m, along with an optional path list.
        uses the opencv library that you can install via `pip install opencv-python` in your terminal
        """

        im = Image.new(
            "RGB",
            (self.zoom * len(self.a[0]), self.zoom * len(self.a)),
            (255, 255, 255),
        )  # Creates a new image of reasonable resolution
        draw = ImageDraw.Draw(im)  # init draw obj
        for i in range(len(self.a)):
            for j in range(len(self.a[i])):
                color = (255, 255, 255)
                r = 0
                if self.a[i][j] == 1:  # if the current pixel is 0, color = black
                    color = (0, 0, 0)
                if i == self.start[0] and j == self.start[1]:  # if location is at start
                    color = (0, 255, 0)
                    r = self.borders
                if i == self.end[0] and j == self.end[1]:  # if location is at end draw
                    color = (0, 255, 0)
                    r = self.borders
                draw.rectangle(
                    (
                        j * self.zoom + r,
                        i * self.zoom + r,
                        j * self.zoom + self.zoom - r - 1,
                        i * self.zoom + self.zoom - r - 1,
                    ),
                    fill=color,
                )
        for u in range(len(self.current_path) - 1):
            """Block of code draws lines that links the grid together."""
            y = self.current_path[u][0] * self.zoom + int(self.zoom / 2)
            x = self.current_path[u][1] * self.zoom + int(self.zoom / 2)
            y1 = self.current_path[u + 1][0] * self.zoom + int(self.zoom / 2)
            x1 = self.current_path[u + 1][1] * self.zoom + int(self.zoom / 2)
            fill = (255, 0, 0) if u % 2 else (128, 128, 0)
            draw.line((x, y, x1, y1), fill=fill, width=5)
        draw.rectangle(
            (0, 0, self.zoom * len(self.a[0]), self.zoom * len(self.a)),
            outline=(0, 255, 0),
            width=2,
        )
        self.images.append(im)

    def make_step(self, temp, k):
        """m is a copy of matrix a
        k is the current step count

        `make_step` advances the frontier (see the gif) of the search space (by checking if m[i][j]==k).
        assigns value k+1 to a box just outside the space
        skips the box if visited (because otherwise the path automatically gets cut off and it'd be a cycle anyways.)
        """
        for i in range(len(temp)):  # number of rows
            for j in range(len(temp[i])):  # number of cols
                if temp[i][j] == k:  # if the position matches the value of k
                    if (
                        i > 0 and temp[i - 1][j] == 0 and self.a[i - 1][j] == 0
                    ):  # if box down is 0
                        temp[i - 1][j] = k + 1
                    if (
                        j > 0 and temp[i][j - 1] == 0 and self.a[i][j - 1] == 0
                    ):  # if box to the left is 0
                        temp[i][j - 1] = k + 1
                    if (
                        i < len(temp) - 1
                        and temp[i + 1][j] == 0
                        and self.a[i + 1][j] == 0
                    ):  # if box up is 0
                        temp[i + 1][j] = k + 1
                    if (
                        j < len(temp[i]) - 1
                        and temp[i][j + 1] == 0
                        and self.a[i][j + 1] == 0
                    ):  # if box right is 0
                        temp[i][j + 1] = k + 1

    def __bfs(self, start):
        """Returns the list of vertices that leads to the shortest path
        run bfs till vertex in vertex list. return path list
        recursively call bfs but exclude that vertex from the list until len(vertices) == 0
        draw path list
        """
        if start == self.end:
            return

        # Create a copy of matrix a populated with 0
        temp = np.zeros(np.shape(self.a))
        i, j = start  # sets the start point
        temp[i][j] = 1  # sets start to 1

        k = 0
        v = None
        while True:
            if len(self.vertices) != 0:
                v = self.return_vertex_reached(temp)
                if v is not None:
                    break
            else:
                # check whether end has been reached
                if temp[self.end] != 0:
                    v = self.end
                    break

            """while the end position has not been reached, and is still empty (hence 0)
            increment k to feed into make_step"""
            k += 1
            self.make_step(temp, k)
            # self.draw_matrix()
        # if some vertex has been reached for some k,
        if len(self.vertices) != 0:
            self.vertices.remove(v)
        k = temp[v]
        i, j = v
        the_path = []
        while k > 1:
            if i > 0 and temp[i - 1][j] == k - 1:
                i, j = i - 1, j
                the_path.append((i, j))
                k -= 1
            elif j > 0 and temp[i][j - 1] == k - 1:
                i, j = i, j - 1
                the_path.append((i, j))
                k -= 1
            elif i < len(temp) - 1 and temp[i + 1][j] == k - 1:
                i, j = i + 1, j
                the_path.append((i, j))
                k -= 1
            elif j < len(temp[i]) - 1 and temp[i][j + 1] == k - 1:
                i, j = i, j + 1
                the_path.append((i, j))
                k -= 1
        self.current_path += the_path[::-1]
        # update self.m by reading current path
        k = len(self.current_path)
        for node in the_path:
            self.m[node] = k + 1
            k += 1
        self.print_m(v, self.m)
        self.__bfs(v)
        # self.draw_matrix()

    def print_m(self, v, m):
        """Helper function to print the maze."""
        print(f"BFS for {v}")
        for i in range(len(m)):
            for j in range(len(m[i])):
                print(str(m[i][j]).ljust(3), end=" ")
            print()
        return

    def save_image(self, name="solution.png"):
        self.images[0].save(name)

#Documentation
if __name__ == "__main__":
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
    start = 1, 1  # define a start point for the maze
    end = 2, 5  # define the end point for the maze
    vertex_list = [(3, 3), (4, 4)]  # put the coordinates of all the gems here
    vertex_list = [
        (8, 3),
        (4, 4),
        (1, 3),
        (8, 1),
    ]  # put the coordinates of all the gems here
    solver = Solver(a, start, vertex_list, end)  # Create solver
    solver.solve_maze()
    images = solver.images
    images[0].save(
        "default_bfs_sol_4.gif",  # change the location because backslash pathing only works on windows
        save_all=True,
        append_images=images[1:],
        optimize=False,
        duration=1,
        loop=0,
    )
    print(f"Final path (len = {len(solver.current_path)}):\n{solver.current_path}")
    print(f"Image array length = {len(solver.images)}")
