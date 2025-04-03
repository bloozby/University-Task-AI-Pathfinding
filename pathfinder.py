import sys
import numpy as np
import re

STUDENT_ID='a1821415'
DEGREE = 'UG'

def printMap(mapp):
    for i in range(np.size(mapp, 0)):
        for j in range(np.size(mapp, 1)):
            if j == np.size(mapp, 1)-1:
                print(mapp[i,j])
            else: 
                print(mapp[i,j] + " ", end = "")

def printVisits(mapp):
    for i in range(np.size(mapp, 0)):
        for j in range(np.size(mapp, 1)):
            if mapp[i,j] == 0:
                printed = "  X"
            elif mapp[i,j] > 0 and mapp[i,j] < 10:
                printed = "  " + str(mapp[i,j])
            elif mapp[i,j] > 9 and mapp[i,j] < 100:
                printed = " " + str(mapp[i,j])
            else:
                printed = str(mapp[i,j])
            
            if j == np.size(mapp, 1)-1:
                print(printed)
            else:
                print(printed + " ", end = "")

def findChildren(pr, pc, mapn):
    currNodeChildren = []

    # Up
    if pr > 0 and mapn[pr - 1, pc] != 'X':  # Ensure it's not an obstacle
        currNodeChildren.append(Child(True, pr - 1, pc, mapn))
    else:
        currNodeChildren.append(Child(False, pr, pc, mapn))

    # Down
    if pr < np.size(mapn, 0) - 1 and mapn[pr + 1, pc] != 'X':  # Ensure it's not an obstacle
        currNodeChildren.append(Child(True, pr + 1, pc, mapn))
    else:
        currNodeChildren.append(Child(False, pr, pc, mapn))

    # Left
    if pc > 0 and mapn[pr, pc - 1] != 'X':  # Ensure it's not an obstacle
        currNodeChildren.append(Child(True, pr, pc - 1, mapn))
    else:
        currNodeChildren.append(Child(False, pr, pc, mapn))

    # Right
    if pc < np.size(mapn, 1) - 1 and mapn[pr, pc + 1] != 'X':  # Ensure it's not an obstacle
        currNodeChildren.append(Child(True, pr, pc + 1, mapn))
    else:
        currNodeChildren.append(Child(False, pr, pc, mapn))

    return currNodeChildren

class Child:
    def __init__(self, isreal, pr, pc, map, parent=None):
        self.isreal = isreal
        self.parent = parent  # Keep track of the parent node
        if isreal:
            self.pr = pr
            self.pc = pc
            self.value = map[pr, pc]
        else:
            self.pr = None
            self.pc = None
            self.value = "X"

    def __repr__(self):
        if self.isreal:
            return f"Child(pr={self.pr}, pc={self.pc}, value={self.value})"
        else:
            return f"Child(isreal=False, value={self.value})"

class Node:
    def __init__(self, isreal, pr, pc, map):
        self.isreal = isreal
        self.pr = pr
        self.pc = pc
        self.value = map[pr, pc]
        self.children = findChildren(pr, pc, map)

        if self.value == "X":
            self.obstacle = True

    def __repr__(self):
        return f"Node(pr={self.pr}, pc={self.pc}, value={self.value}, children={self.children})"
    
def appendChildren(appendee, children_list):
    appending = True

    for i in range(len(children_list)):
        if children_list[i].isreal == False:
            appending = False
        else:
            appending = True
            
        for j in range(len(appendee)):
            if (children_list[i].pr == appendee[j].pr) and (children_list[i].pc == appendee[j].pc):
                appending = False
        if appending == True:
            appendee.append(children_list[i])


# BFS Algorithm
def BFS(sp, ep, ary, mode):
    start_node = Node(True, sp[1] - 1, sp[0] - 1, ary)  # starting from (startX, startY)
    moveMap = np.array(ary)
    moveMap[start_node.pr, start_node.pc] = "*"  # Mark the start on the map

    # Initialize the fringe with the start node
    fringe = []
    fringe.append(Child(True, start_node.pr, start_node.pc, ary, parent=None))

    # Initialize a 3D visited matrix (height x width x 3), the 3 channels:
    # 0: visit count, 1: first visited, 2: last visited
    visited = np.zeros((np.size(ary, 0), np.size(ary, 1), 3), dtype=int)  # Initialize all as 0
    visited[start_node.pr, start_node.pc, 0] = 1  # The start node is visited once
    visited[start_node.pr, start_node.pc, 1] = 1  # Mark the start node as first visited
    visited[start_node.pr, start_node.pc, 2] = 1  # Start node's first visit time

    solution = False
    path = []

    # BFS Loop
    visitno = 2  # Starting from the 2nd visit time for subsequent visits
    destination_found = False  # Flag to track if the destination has been found

    while fringe:
        curr_child = fringe.pop(0)  # Get the first child from the fringe
        currNode = Node(True, curr_child.pr, curr_child.pc, ary)

        # If we've reached the end point, backtrack the path
        for i in range(len(currNode.children)):
            child = currNode.children[i]
            if (child.pr, child.pc) == (ep[1] - 1, ep[0] - 1):
                solution = True
                if not destination_found:
                    # Mark both first and last visit times the same for the destination node
                    visited[child.pr, child.pc, 1] = visitno  # First visit time
                    visited[child.pr, child.pc, 2] = visitno  # Last visit time
                    destination_found = True  # Prevent further updates to the destination
                    moveMap[child.pr, child.pc] = "*"
                # Backtrack to find the full path
                while curr_child:
                    path.append((int(curr_child.pr), int(curr_child.pc)))  # Convert to Python int
                    moveMap[curr_child.pr, curr_child.pc] = "*"
                    curr_child = curr_child.parent
                path.reverse()  # Reverse the path to get it from start to end
                break  # Immediately stop further exploration after finding the destination

        # Append children to fringe
        for child in currNode.children:
            if child.isreal and ary[child.pr][child.pc] != 'X':
                # Increment the visit count for the node
                if visited[child.pr, child.pc, 0] == 0:
                    # If not visited yet, mark it as visited
                    visited[child.pr, child.pc, 0] = 1
                    visited[child.pr, child.pc, 1] = visitno  # First visit time
                    fringe.append(Child(True, child.pr, child.pc, ary, parent=curr_child))
                else:
                    # If already visited, increment the visit count and update last visit time
                    visited[child.pr, child.pc, 0] += 1
                    visited[child.pr, child.pc, 2] = visitno  # Last visit time

                visitno += 1  # Increment visit time

        # Break if we already found the solution
        if solution:
            break

    # Ensure last visit for destination is set to correct time (if not already updated)
    if visited[ep[1] - 1, ep[0] - 1, 2] != visitno - 1:
        visited[ep[1] - 1, ep[0] - 1, 2] = visitno - 1

    # Output results
    if mode == "release":
        if solution:
            printMap(moveMap)
            return None
        else:
            print("null")
            return None
    else:
        if solution:
            print("path:")
            printMap(moveMap)
            print("#visits:")
            printVisits(visited[:,:,0])
            print("first visits:")
            printVisits(visited[:,:,1])
            print("last visits:")
            printVisits(visited[:,:,2])
            return None
        else:
            print("path:")
            print("null")
            print("#visits:")
            print("...")
            print("first visits:")
            print("...")
            print("last visits:")
            print("...")
            return None


#UCS Algorithm

#A* Algorithm


if __name__ == "__main__":
    ## >>>> python pathfinder.py [mode] [map] [algorithm] [heuristic]
    # MODE can either be debug or release 
    mode = sys.argv[1]

    # check input for "MODE" is correct
    if mode != 'debug' and mode != 'release':
        sys.exit("Error: 'mode' variable incorrect")

    # MAP specifies the path to map, which is a text file formatted according to this example
    map = sys.argv[2]

    # check input for "MAP" is  text file
    if map.endswith(".txt") == False:
        sys.exit("Error: 'map' variable incorrect (must be path to text file)")

    # read map file and store variables
    try:
        txt = open(map, "r")
    except:
        sys.exit("Error: txt wouldnt open")

    #check if txt document is correct
    
    #store initial values
    mapSize = np.array(re.findall("(\d+)", txt.readline()))
    startPoint = np.array(re.findall("(\d+)", txt.readline()))
    endPoint = np.array(re.findall("(\d+)", txt.readline()))
    
    mapSize = mapSize.astype('i')
    startPoint = startPoint.astype('i')
    endPoint = endPoint.astype('i')
    
    #store map
    mapArray = np.zeros((mapSize[0], mapSize[1]), 'U')

    for i in range(mapSize[0]):
        mapArray[i,:] = np.array(re.findall("(\d+|X)", txt.readline().strip()))


    # ALGORITHM specifies the search algorithm to use, with the possible values of bfs, ucs, and astar
    algorithm = sys.argv[3]

    #check if input is valid
    if algorithm != 'bfs' and algorithm != 'ucs' and algorithm != 'astar':
        sys.exit("Error: 'algorithm' variable incorrect")

    # HEURISTIC specifies the heuristic to use for the A* search, with the possible values of euclidean and manhattan. This input is ignored for BFS and UCS.
    heuristic = sys.argv[4]

    if heuristic != 'euclidean' and heuristic != 'manhattan' and algorithm == 'astar':
        sys.exit("Error: 'heuristic' variable incorrect")


    # run depending
    if algorithm == 'bfs':
        BFS(startPoint, endPoint, mapArray, mode)
