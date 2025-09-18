"""astar.py
Simple, well-documented A* pathfinding implementation for a 2D grid.
Grid values: 0 = free, 1 = obstacle.
Returns a list of (row, col) coordinates from start to goal (inclusive), or [] if no path.
"""
import heapq
from typing import List, Tuple, Optional

Grid = List[List[int]]
Coord = Tuple[int, int]

def heuristic(a: Coord, b: Coord, method: str = 'manhattan') -> float:
    (x1, y1), (x2, y2) = a, b
    if method == 'euclidean':
        return ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5
    # default: Manhattan
    return abs(x1 - x2) + abs(y1 - y2)

def neighbors(pos: Coord, grid: Grid, allow_diagonal: bool = False) -> List[Coord]:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    r, c = pos
    steps = [(-1,0),(1,0),(0,-1),(0,1)]
    if allow_diagonal:
        steps += [(-1,-1),(-1,1),(1,-1),(1,1)]
    result = []
    for dr, dc in steps:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
            result.append((nr, nc))
    return result

def reconstruct_path(came_from: dict, current: Coord) -> List[Coord]:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def astar(grid: Grid, start: Coord, goal: Coord, allow_diagonal: bool = False, heuristic_method: str = 'manhattan') -> List[Coord]:
    if start == goal:
        return [start]
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    sr, sc = start
    gr, gc = goal
    if not (0 <= sr < rows and 0 <= sc < cols and 0 <= gr < rows and 0 <= gc < cols):
        raise ValueError('start or goal out of bounds')
    if grid[sr][sc] != 0 or grid[gr][gc] != 0:
        return []  # no path if start/goal is blocked

    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal, heuristic_method), 0, start))
    came_from = {}
    g_score = {start: 0}
    closed = set()

    while open_set:
        f, current_g, current = heapq.heappop(open_set)
        if current in closed:
            continue
        if current == goal:
            return reconstruct_path(came_from, current)
        closed.add(current)

        for nbr in neighbors(current, grid, allow_diagonal):
            tentative_g = g_score[current] + (1.4142 if (abs(nbr[0]-current[0])==1 and abs(nbr[1]-current[1])==1) else 1)
            if tentative_g < g_score.get(nbr, float('inf')):
                came_from[nbr] = current
                g_score[nbr] = tentative_g
                fscore = tentative_g + heuristic(nbr, goal, heuristic_method)
                heapq.heappush(open_set, (fscore, tentative_g, nbr))
    return []  # no path found

if __name__ == '__main__':
    # tiny demo when run directly
    demo_grid = [
        [0,0,0,0,0,0,0],
        [0,1,1,1,1,0,0],
        [0,0,0,1,0,0,0],
        [0,1,0,0,0,1,0],
        [0,0,0,1,0,0,0],
    ]
    start = (0,0)
    goal = (4,6)
    path = astar(demo_grid, start, goal)
    print('Found path:' if path else 'No path found')
    print(path)
