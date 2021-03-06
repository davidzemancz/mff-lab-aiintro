Implement monotone heuristics for the A* algorithm running on subgraphs of the following infinite grids.

* Grid2D: The classic two-dimensional grid
* Grid3D: The classic three-dimensional grid
* GridDiagonal2D: The two-dimensional grid that includes diagonals (including {(0,0), (1,1)} and {(0,1), (1,0)})
* GridAllDiagonal3D: The three-dimensional grid containing both face and space diagonals (including, for example, {(0,0,0), (1,1,0)} and {(0,0,0), (1,1,1)})
* GridFaceDiagonal3D: The three-dimensional grid containing face diagonals but not space ones (for example, it contains {(0,0,0), (1,1,0)} but does not contain {(0,0,0), (1,1,1)} )
* GridKnight2D: Edges correspond exactly to the movement of the knight on the chessboard (for example, it contains {(0,0), (2,1)} and {(0,0), (-1,2)} but it does not include {(0,0), (1,0)})

A subgraph is given by an oracle that decides whether an edge of the grid is presented or removed from the subgraph.

Download the git repository https://gitlab.mff.cuni.cz/finkj1am/introai.git and implement all functions in heuristics.py. Submit only the heuristics.py file to ReCodex. Please, do not change the name of the file when submitting. You can also edit other files while debugging, but keep in mind that recodex will not take these changes into account.

Recodex tests are the same as in the file informed_search_tests.py. The expected heuristics visit at most million vertices in each test, and inefficient heuristics fails to find the shortest path within time limit set in ReCodex. All tests should run between 1 and 3 minutes depending on speed of your computer.

Hints:
* Observation: If an integer is larger than 5.5, then it is at least 6.
* The command "ulimit -v" may be useful to limit amount of memory the program can allocate to prevent swapping and other problems related to insufficient amount of memory.
* The reference time provided by the script informed_search_tests.py is the running time on computer Intel(R) Core(TM) i5-7200U CPU @ 2.50GHz with 8 GB RAM. Time limit on Recodex is 60 seconds for each grid but its computer is a little bit slower.
