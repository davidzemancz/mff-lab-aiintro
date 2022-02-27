# TODO: Implement more efficient monotonic heuristic
#
# Every function receive coordinates of two grid points returns estimated distance between them.
# Each argument is a tuple of two or three integer coordinates.
# See file task.md for description of all grids.

import math

def grid_2D_heuristic(current, destination):
    return abs((current[0]-destination[0])) + abs((current[1]-destination[1]))

def grid_diagonal_2D_heuristic(current, destination):
    return max(abs((current[0]-destination[0])), abs((current[1]-destination[1])))

def grid_3D_heuristic(current, destination):
    return abs((current[0]-destination[0])) + abs((current[1]-destination[1])) + abs((current[2]-destination[2]))

def grid_all_diagonal_3D_heuristic(current, destination):
    return max(abs((current[0]-destination[0])), abs((current[1]-destination[1])), abs((current[2]-destination[2])))

def grid_face_diagonal_3D_heuristic(current, destination):
    val = 0
    d0 = abs((current[0]-destination[0]))
    d1 = abs((current[1]-destination[1]))
    d2 = abs((current[2]-destination[2]))

    dmax = max(d0, d1,d2)
    sum = d0 + d1 + d2

    if sum - dmax <= dmax: val = dmax
    else: val = math.ceil(sum / 2)

    return val

def grid_knight_2D_heuristic(current, destination):
    val = 0
    
    d0 = abs((current[0]-destination[0]))
    d1 = abs((current[1]-destination[1]))

    dmax = max(d0, d1)
    dmin = min(d0, d1)

    if dmin * 2 < dmax:
        val = math.ceil(dmax / 2)
    else:
        val = math.ceil((dmax + dmin) / 3)

    return val
