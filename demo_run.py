# demo_run.py
# Runs the astar algorithm on example grids and saves a PNG showing the grid and the path.
import astar as A
import numpy as np
import matplotlib
matplotlib.use('Agg')  # do not require a display
import matplotlib.pyplot as plt
import os

def draw_grid(grid, path, filename='demo_output.png'):
    grid = np.array(grid)
    rows, cols = grid.shape
    # 0 = free, 1 = obstacle
    # Create an image array: 0=free (white), 1=obstacle (black)
    img = np.zeros((rows, cols, 3), dtype=float) + 1.0  # start white
    # obstacles
    img[grid == 1] = [0.0, 0.0, 0.0]
    # path overlay: mark path cells with blue-ish shade
    for (r, c) in path:
        img[r, c] = [0.2, 0.6, 1.0]
    # start/goal
    if path:
        sr, sc = path[0]
        gr, gc = path[-1]
        img[sr, sc] = [0.0, 1.0, 0.0]  # start green
        img[gr, gc] = [1.0, 0.0, 0.0]  # goal red

    plt.figure(figsize=(cols/2, rows/2))
    plt.imshow(img, interpolation='nearest')
    plt.axis('off')
    plt.title('A* demo - blue = path, green = start, red = goal, black = obstacle')
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print('Saved demo image to', filename)

def main():
    demo_grid = [
        [0,0,0,0,0,0,0,0,0,0],
        [0,1,1,1,1,1,0,1,1,0],
        [0,0,0,1,0,0,0,1,0,0],
        [0,1,0,0,0,1,0,1,0,0],
        [0,0,0,1,0,0,0,0,0,0],
        [0,1,0,0,0,1,1,1,1,0],
        [0,0,0,0,0,0,0,0,0,0],
    ]
    start = (0,0)
    goal = (6,9)
    path = A.astar(demo_grid, start, goal, allow_diagonal=True)
    if not path:
        print('No path found for demo.')
    else:
        print('Demo path length:', len(path))
    out = os.path.join(os.path.dirname(__file__), 'demo_output.png')
    draw_grid(np.array(demo_grid), path, out)

if __name__ == '__main__':
    main()
