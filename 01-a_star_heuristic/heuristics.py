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
    if current[0] != destination[0] and current[1] != destination[1] and current[2] != destination[2]:
        val = max(
            max(abs((current[0]-destination[0])), abs((current[1]-destination[1])))
            ,max(abs((current[0]-destination[0])), abs((current[2]-destination[2])))
            ,max(abs((current[1]-destination[1])), abs((current[2]-destination[2]))))
    else: 
        val = max(abs((current[0]-destination[0])), abs((current[1]-destination[1])), abs((current[2]-destination[2])))
    return val

def grid_knight_2D_heuristic(current, destination):
    return max(abs((current[0]-destination[0])) - abs((current[1]-destination[1])), abs((current[1]-destination[1])) - abs((current[0]-destination[0])))
