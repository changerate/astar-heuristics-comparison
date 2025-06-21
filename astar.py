# Carlos Vargas 
# June 21st, 2025

# CS 4200 - Artificial Intelligence
# Professor Daisy Tang 
# California State Polytechnic University - Pomona

# -----------------------------------------------------------------

import heapq
import os # For clearing the terminal

def AStar8PuzzleAlgorithm(initialNode, boardHeight, boardLength):
    goalState = tuple(tuple(row) for row in [[0,1,2],[3,4,5],[6,7,8]])
    exploredNodes = set()

    # Initialize the frontier as a priority queue (see sortPriorityQueueByFn())
    frontier = []
    heapq.heappush(frontier, initialNode)
    frontierStates = {initialNode.stateHash: initialNode}   # For quicker searcher; we
                                                            # use hashes. This makes
                                                            # storage more cost effective
                                                            # and search decreases. 
    # Explore the frontier while there's still nodes 
    while frontier: 
        currentNode = heapq.heappop(frontier)
        del frontierStates[currentNode.stateHash]
        
        print("▊ Current Depth:", currentNode.g)
        
        if currentNode.stateHash == goalState:
            return currentNode.g 
        
        exploredNodes.add(currentNode.stateHash)
        successorNodes = findSuccessorNodes(currentNode, boardLength, boardHeight)

        # Exploring each successor node
        for successorNode in successorNodes:
            successorHash = successorNode.stateHash
            
            if successorHash in exploredNodes:  # Check if it's in the explored list
                continue
            if successorHash in frontierStates:     # Check if it's in the frontier list
                existingNode = frontierStates[successorHash]
                if successorNode.g < existingNode.g:
                    existingNode.g = float('inf')  # Mark as invalid
                    heapq.heappush(frontier, successorNode)
                    frontierStates[successorHash] = successorNode
            else:  # Add it to the frontier list
                heapq.heappush(frontier, successorNode)
                frontierStates[successorHash] = successorNode

    return "ERROR" 





'''
@Input: exampleNode = [[0,1,2],[3,4,5],[6,7,8]], where the rows and columns can vary
@Output: integer sum of the manhattan distances 
'''
def summedManhattanDistance(state): 
    sumOfDistances = 0 
    
    for row in range(len(state)):
        for column in range(len(state[0])):
            tileFaceValue = state[row][column]
            if tileFaceValue != 0:
                goalRow, goalCol = GOAL_POSITIONS[tileFaceValue]
                sumOfDistances += abs(row - goalRow) + abs(column - goalCol)
    return sumOfDistances




'''
@Input: currentNode = [boardLength X boardHeight]
@Input: boardLength
@Input: boardHeight
'''
def findSuccessorNodes(currentNode, boardLength, boardHeight):
    successors = []
    state = currentNode.state
    # Find empty position
    emptyPos = currentNode.emptyPos
    row, col = emptyPos

    # The possibility of moves up down right left
    moves = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    
    for directionalOffsetRow, directionalOffsetCol in moves:
        newRow, newCol = row + directionalOffsetRow, col + directionalOffsetCol
        
        if 0 <= newRow < boardHeight and 0 <= newCol < boardLength: # Check bounds
            # Create new state by swapping
            newState = [list(row) for row in state]  # Deep copy
            newState[row][col], newState[newRow][newCol] = newState[newRow][newCol], newState[row][col]
            
            # Create new node
            newNode = Node(state=newState, g=currentNode.g + 1)
            successors.append(newNode)

    return successors




def getNextInitialPuzzle(puzzleIndex, puzzleDatabaseFile, boardHeight, boardLength, puzzleFileIndex):
    initialNode = [[0 for _ in range(boardLength)] for _ in range(boardHeight)]

    # Fill out the initialNode with the given numbers from next puzzle
    while puzzleIndex < boardHeight * boardLength: 
        char = puzzleDatabaseFile[puzzleFileIndex]
        puzzleFileIndex += 1

        # If the current character is a number, add it to the initialNode
        if char in '012345678' and puzzleIndex < boardHeight * boardLength:
            initialNode[puzzleIndex // boardHeight][puzzleIndex % boardLength] = int(char)
            puzzleIndex += 1

    return (initialNode, puzzleFileIndex)




def AStarIDSComparisonWithFile(boardHeight, boardLength):
    listOfCosts = set()

    # read file 
    puzzleDatabaseFile = ""
    with open('project-1-instructions/Length16.txt', 'r') as file:
        puzzleDatabaseFile = file.read()


    # While there is still a puzzle to be worked on: 
    puzzleFileIndex = 0
    while puzzleFileIndex < len(puzzleDatabaseFile):
        indexAndPuzzleTuple = getNextInitialPuzzle(0, puzzleDatabaseFile, boardHeight, boardLength, puzzleFileIndex)
        puzzleFileIndex = indexAndPuzzleTuple[1]

        initialNode = Node(state = indexAndPuzzleTuple[0])
        listOfCosts.add(AStar8PuzzleAlgorithm(initialNode, boardHeight, boardLength))

    return listOfCosts




class Node: 
    def __init__(self, state, g=0):
        self.state = state
        self.g = g  # Think about g(n) as the depth of the search, or the number of moves
        self.stateHash = tuple(tuple(row) for row in state)  # Immutable hash for set operations
        self.h = summedManhattanDistance(state)
        self.emptyPos = self.findEmptyPos()

    def f(self):
        return self.g + self.h

    def findEmptyPos(self):
        for row in range(len(self.state)):
            for col in range(len(self.state[0])):
                if self.state[row][col] == 0:
                    return (row, col)
        return None

    # For heapq implementation 
    def __lt__(self, other):
        # For heapq comparison - compare by f() value first, then by g value
        if self.f() != other.f():
            return self.f() < other.f()
        return self.g > other.g  # Prefer higher g (deeper) for tie-breaking
    
    def __eq__(self, other):
        return self.stateHash == other.stateHash



def getUserPreferences():
    puzzlePreference = 1
    inputPreference = 1
    invalidInput = True

    while(invalidInput):
        puzzlePreference = input(
            "Select:\n"
            "[1] Single Test Puzzle\n"
            "[2] Multi-Test Puzzle\n"
            "[3] Exit\n"
            "Your choice: "
        )

        # ---- Handle errors with input
        try:
            puzzlePreference = int(puzzlePreference)
            if (1 > puzzlePreference or puzzlePreference > 3):
                invalidInput = True
                print("\n▊ ERROR: Please only input an integer (1, 2, or 3) followed by a return\n")
            else:
                invalidInput = False
        except:
            print("\n▊ ERROR: Please only input an integer (1, 2, or 3) followed by a return\n")
        
    invalidInput = True
    while(invalidInput):
        inputPreference = input(
            "\nSelect Input Method:\n"
            "[1] Random\n"
            "[2] File\n"
            "Your choice: "
        )
        # ---- Handle errors with input
        try:
            inputPreference = int(inputPreference)
            if (1 > inputPreference or inputPreference > 2):
                invalidInput = True
                print("\n▊ ERROR: Please only input an integer (1 or 2) followed by a return")
            else:
                invalidInput = False
        except:
            print("\n▊ ERROR: Please only input an integer (1 or 2) followed by a return")
    
    return (puzzlePreference, inputPreference)



# =====================================================================
#                               MAIN
# =====================================================================
if __name__ == "__main__":
    def clear_terminal():
        os.system('cls' if os.name == 'nt' else 'clear')
    clear_terminal()

    boardHeight = 3
    boardLength = 3
    GOAL_POSITIONS = {i: (i//boardHeight, i%boardLength) for i in range(boardHeight*boardLength)}

    print("\nHello, welcome to the 8-puzzle problem solver using the A* algorithm.\n")
    puzzlePreference, inputPreference = getUserPreferences()    
    
    # print("------------------------------------------------")
    # print("Cost of algorithm:", AStarIDSComparisonWithFile(boardHeight, boardLength))
    # print("------------------------------------------------")
    # # AStarIDSComparisonWithInput()
