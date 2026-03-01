# Pathfinder — BFS, UCS, and A* Search (Grid Maps)

A Python command-line pathfinding tool implementing **Breadth-First Search (BFS)**, **Uniform Cost Search (UCS)**, and **A\*** on a grid-based map with obstacles and terrain costs.

---


---

##  Features

- **BFS** (unweighted shortest path in number of steps)
- **UCS** (least-cost path using terrain-based movement costs)
- **A\*** (least-cost path + heuristic guidance)
- Supports two heuristics for A\*: **Manhattan** and **Euclidean**
- Two output modes:
  - `release` → prints only the final path or `null`
  - `debug` → prints the path + visit statistics matrices

---

## Map Format

The program reads a plain-text map file.

### Expected File Structure

1. Map size (rows cols)
2. Start point (x y)
3. End point (x y)
4. Grid rows of cells (`X` for obstacle, digits for terrain)

### Example

<table border="0">
  <tr>
    <td>5</td><td>5</td>
  </tr>
  <tr>
    <td>1</td><td>1</td>
  </tr>
  <tr>
    <td>1</td><td>1</td><td>1</td><td>1</td><td>1</td>
  </tr>
  <tr>
    <td>1</td><td>X</td><td>2</td><td>2</td><td>1</td>
  </tr>
  <tr>
    <td>1</td><td>1</td><td>3</td><td>X</td><td>1</td>
  </tr>
  <tr>
    <td>1</td><td>1</td><td>1</td><td>1</td><td>1</td>
  </tr>
  <tr>
    <td>1</td><td>1</td><td>1</td><td>1</td><td>1</td>
  </tr>
</table>
### Cell Meanings

- `X` → obstacle (impassable)
- `0–9...` → terrain value (affects movement cost in UCS and A*)

---

##  Algorithms Implemented

###  BFS (`bfs`)
- Explores nodes level-by-level (FIFO queue).
- Finds the path with the **fewest steps**.
- Ignores terrain costs.

---

###  UCS (`ucs`)
- Expands the node with the **lowest cumulative path cost**.
- Movement cost rule:
  - If moving to an equal or lower value cell → cost = `1`
  - If moving to a higher value cell → cost = `(height_difference + 1)`

Finds the true least-cost path.

---

###  A* (`astar`)
- Combines UCS cost and heuristic:
    f(n) = g(n) + h(n)
  

- Supported heuristics:
- `manhattan` → `|dx| + |dy|`
- `euclidean` → `sqrt(dx² + dy²)`

Heuristic guides search toward the goal to improve efficiency.

---

## Usage

Run with:

python pathfinder.py [mode] [map] [algorithm] [heuristic]

### Arguments

| Argument | Options | Notes |
|----------|----------|-------|
| `mode` | `debug` or `release` | Controls output verbosity |
| `map` | Path to `.txt` map file | Required |
| `algorithm` | `bfs`, `ucs`, `astar` | Required |
| `heuristic` | `manhattan`, `euclidean` | Only used when `algorithm=astar` |

---

## Example Commands

### BFS (Release Mode)
  python pathfinder.py release maps/map1.txt bfs

### UCS (Debug Mode)
  python pathfinder.py debug maps/map1.txt ucs
### A* with Manhattan Heuristic
  python pathfinder.py release maps/map1.txt astar manhattan
### A* with Manhattan Heuristic
  python pathfinder.py debug maps/map1.txt astar euclidean

---

## Output Format

### Release Mode

- If a solution exists → prints the map with `*` marking the path
- If no solution exists → prints:

Example:

<table border="0">
  <tr>
    <td>*</td><td>1</td><td>1</td><td>1</td>
  </tr>
  <tr>
    <td>*</td><td>X</td><td>1</td><td>1</td>
  </tr>
  <tr>
    <td>*</td><td>*</td><td>*</td><td>1</td>
  </tr>
  <tr>
    <td>1</td><td>1</td><td>*</td><td>*</td>
  </tr>
</table>


### 🔹 Debug Mode

Prints:

1. `path:` → map with `*`
2. `#visits:` → visit count per cell
3. `first visits:` → first visit timestamp per cell
4. `last visits:` → last visit timestamp per cell

If no solution exists:

path: null

... placeholders for visit tables (matching spec expectations)

---

##  Implementation Details

- Coordinates from input file are converted for internal row/column indexing.
- Neighbours are expanded in this order:
  - Up
  - Down
  - Left
  - Right
- Obstacles (`X`) are never expanded.
- Path reconstruction uses parent references stored in child nodes.
- A 3D `visited` matrix tracks:
  - Visit count
  - First visit time
  - Last visit time

---

##  File Structure

pathfinder.py   # Implementation (BFS, UCS, A*, parsing, output formatting)
