Pathfinder — BFS, UCS, and A* Search (Grid Maps)

A Python command-line pathfinding tool implementing Breadth-First Search (BFS), Uniform Cost Search (UCS), and A* on a grid-based map with obstacles and terrain costs.

Features

- BFS (unweighted shortest path in number of steps)

- UCS (least-cost path using terrain-based movement costs)

- A* (least-cost path + heuristic guidance)

- Supports two heuristics for A*: Manhattan and Euclidean

- Two output modes:

    release → prints only the final path or null

    debug → prints the path + visit statistics matrices

Map Format

  The program reads a plain-text map file.
  
  Expected file structure
  
  Map size (rows, cols)
  
  Start point (x, y)
  
  End point (x, y)
  
  Grid rows of cells (X for obstacle, digits for terrain)

Example layout:

  5 5
  1 1
  5 5
  1 1 1 1 1
  1 X 2 2 1
  1 1 3 X 1
  1 1 1 1 1
  1 1 1 1 1

Cell meanings

  X → obstacle (impassable)
  
  0–9... → terrain value (affects cost in UCS/A*)

Algorithms
BFS (bfs)

  Explores level-by-level (FIFO queue).
  
  Finds the path with the fewest steps (ignores terrain costs).

UCS (ucs)

  Explores the node with the lowest cumulative path cost first.
  
  Movement cost rule used in this implementation:
  
  If moving to an equal/lower value cell: cost = 1
  
  If moving to a higher value cell: cost = (height_difference + 1)

A* (astar)

  Uses UCS cost + heuristic estimate:
  
    f(n) = g(n) + h(n)
  
  Heuristic options:
  
    manhattan → |dx| + |dy|
    
    euclidean → sqrt(dx² + dy²)

 Usage

Run with:

python pathfinder.py [mode] [map] [algorithm] [heuristic]

Arguments
  Argument	Options	Notes
  mode	debug or release	Controls output verbosity
  map	path to .txt map file	Required
  algorithm	bfs, ucs, astar	Required
  heuristic	manhattan, euclidean	Only used when algorithm=astar

Examples
BFS (release)
  python pathfinder.py release maps/map1.txt bfs
UCS (debug)
  python pathfinder.py debug maps/map1.txt ucs
A* with Manhattan heuristic
  python pathfinder.py release maps/map1.txt astar manhattan
A* with Euclidean heuristic (debug)
  python pathfinder.py debug maps/map1.txt astar euclidean

Output Format
Release Mode

  If a solution exists: prints the map with * marking the path
  
  If no solution exists: prints null

Example:

* 1 1 1
* X 1 1
* * * 1
1 1 * *


Debug Mode

If a solution exists, prints:

path: → map with *

#visits: → visit count per cell

first visits: → visit order when a cell was first discovered

last visits: → last time a cell was considered/updated

If no solution exists, prints:

path: null

... placeholders for visit tables (matching spec expectations)

Implementation Notes

Coordinates from the file are read as (x, y) but internally converted for row/column indexing.

Neighbours are expanded in fixed order:

Up, Down, Left, Right

Obstacles (X) are never expanded.

Path reconstruction is done via parent pointers stored in Child objects.

 Files
pathfinder.py   # Implementation (BFS, UCS, A*, parsing, output formatting)
