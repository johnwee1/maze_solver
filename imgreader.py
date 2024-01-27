# copied from chatgpt

from PIL import Image
import numpy as np
import sys
from Solvers.functionizedbfs import Solver

np.set_printoptions(threshold=sys.maxsize, linewidth=400)

# Open the image
image_path = "maze.png"
image = np.array(Image.open(image_path), dtype=np.intc)  # shape in (RGBA)
square_size = 10  # 10px size per box
c = square_size // 2  # offset

white = np.array([255, 255, 255], dtype=np.intc)
black = np.array([0, 0, 0], dtype=np.intc)

# square is 10/10
height = int((image.shape[0] / 10))
width = int((image.shape[1] / 10))
res = np.zeros((height, width), dtype=np.intc)
k = 0
for h in range(height):
    for w in range(width):
        pixel_color = image[h * square_size + c, w * square_size + c, :3]
        if np.array_equal(pixel_color, white):
            res[w, h] = 0
        if np.array_equal(pixel_color, black):
            res[w, h] = 1

start = (1, 1)
end = (39, 39)
# print(res)
s = Solver(res, start, [], end)
s.solve_maze()
s.save_image()
