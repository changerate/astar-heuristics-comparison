# Carlos Vargas 
# June 21st, 2025

# CS 4200 - Artificial Intelligence
# Professor Daisy Tang 
# California State Polytechnic University - Pomona

# -----------------------------------------------------------------

import heapq
import random 
import os # For clearing the terminal

boardHeight = 3
boardLength = 3
GOAL_POSITIONS = {i: (i//boardHeight, i%boardLength) for i in range(boardHeight*boardLength)}
    # This calculates the "goal" positions for any tile given 
    # -- used in the manhattan distance function





# ---------------------------------------------------------------------
#                              node class 
# ---------------------------------------------------------------------




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







# ---------------------------------------------------------------------
#                              algorithms
# ---------------------------------------------------------------------






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
        
        # print("▊ Current Depth:", currentNode.g)
        
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



def AStarHeuristicComparisonWithFile(boardHeight, boardLength):
    listOfCosts = set()

    filename = input("\nEnter the destination of the file containing ALL the puzzles to be solved: ")
    
    # read file 
    puzzleDatabaseFile = ""
    with open(filename, 'r') as file:
        puzzleDatabaseFile = file.read()


    # While there is still a puzzle to be worked on: 
    puzzleFileIndex = 0
    while puzzleFileIndex < len(puzzleDatabaseFile):
        indexAndPuzzleTuple = getNextPuzzleFromFileString(0, puzzleDatabaseFile, boardHeight, boardLength, puzzleFileIndex)
        puzzleFileIndex = indexAndPuzzleTuple[1]

        initialNode = Node(state = indexAndPuzzleTuple[0])
        listOfCosts.add(AStar8PuzzleAlgorithm(initialNode, boardHeight, boardLength))

    return listOfCosts






# ---------------------------------------------------------------------
#                              user inputs 
# ---------------------------------------------------------------------






def gracefullyGetUserPreferences():
    puzzleAmntPref = 1
    inputPreference = 1
    invalidInput = True

    # -------- Get puzzle solve type
    while (invalidInput):
        puzzleAmntPref = input(
            "Select:\n"
            "[1] Single Test Puzzle\n"
            "[2] Multi-Test Puzzle\n"
            "[3] Exit\n"
            "Your choice: "
        )

        # ---- Handle errors with input
        try:
            puzzleAmntPref = int(puzzleAmntPref)
            if (1 > puzzleAmntPref or puzzleAmntPref > 3):
                invalidInput = True
                print("\n▊ ERROR: Please only input an integer (1, 2, or 3) followed by a return\n")
            else:
                invalidInput = False
                if puzzleAmntPref == 3:
                    print("Exiting program.")
                    return (None, None, None)
        except:
            print("\n▊ ERROR: Please only input an integer (1, 2, or 3) followed by a return\n")
        
    # -------- Get input method
    invalidInput = True
    while (invalidInput):
        inputPreference = input(
            "\nSelect Input Method:\n"
            "[1] Random\n"
            "[2] File\n"
            "[3] Manual input\n"
            "Your choice: "
        )
        # ---- Handle errors with input
        try:
            inputPreference = int(inputPreference)
            if (1 > inputPreference or inputPreference > 3):
                invalidInput = True
                print("\n▊ ERROR: Please only input an integer (1 or 3) followed by a return")
            else:
                invalidInput = False
        except:
            print("\n▊ ERROR: Please only input an integer (1 or 3) followed by a return")

    # -------- Get heuristic function
    invalidInput = True
    while (invalidInput):
        heuristicPreference = input(
            "\nSelect H Function:\n"
            "[1] H1\n"
            "[2] H2\n"
            "Your choice: "
        )
        # ---- Handle errors with input
        try:
            heuristicPreference = int(heuristicPreference)
            if (1 > heuristicPreference or heuristicPreference > 2):
                invalidInput = True
                print("\n▊ ERROR: Please only input an integer (1 or 2) followed by a return")
            else:
                invalidInput = False
        except:
            print("\n▊ ERROR: Please only input an integer (1 or 2) followed by a return")
    
    return [puzzleAmntPref, inputPreference, heuristicPreference]




"""
Generate a random puzzle with integers between 0 and boardLength * boardHeight inclusive 
"""
def getRandomPuzzle():
    puzzle = [[0 for _ in range(boardLength)] for _ in range(boardHeight)]
        
    listOfNums = []
    for i in range(boardHeight*boardLength):
        listOfNums.append(i)
    random.shuffle(listOfNums)
    
    for row in range(boardHeight):
        for col in range(boardLength):
            puzzle[row][col] = listOfNums[0]
            listOfNums.remove(listOfNums[0])
    
    # --- print puzzle for testing
    # for row in range(boardHeight):
    #     for col in range(boardLength):
    #         print(puzzle[row][col], end=' ')
    #     print("\n")
    
    return Node(state = puzzle)

   
   
    
def getInitialPuzzlesFromFiles():
    endOfFileNode = Node(state = [[0 for _ in range(boardLength)] for _ in range(boardHeight)])
        # this means the end of the file wsa reached and this initial node is all zeros
    filename = input("\nEnter the destination of the file containing ALL the puzzles to be solved: ")
    initialPuzzleNodes = []
    
    # read file - handle errors 
    puzzleFileAsString = ""
    try: 
        with open(filename, 'r') as file:
            puzzleFileAsString = file.read()
    except:
        print("Can't find that file. Exiting")
        exit()
    
    # While there is still a puzzle to be read from the file
    fileIndex = 0
    while fileIndex < len(puzzleFileAsString):
        initialNode, fileIndex = getNextPuzzleFromFileString(puzzleFileAsString, boardHeight, boardLength, fileIndex)
        if initialNode == endOfFileNode:
            continue
        initialPuzzleNodes.append(initialNode)

    return initialPuzzleNodes

    


def getNextPuzzleFromFileString(puzzleFileAsString, boardHeight, boardLength, fileIndex):
    initialState = [[0 for _ in range(boardLength)] for _ in range(boardHeight)]
    puzzleIndex = 0
    includedNums = set()
    for x in range(boardHeight * boardLength):
        includedNums.add(str(x))
    
    # Fill out the initialState with the given numbers from next puzzle
    while puzzleIndex < boardHeight * boardLength and fileIndex < len(puzzleFileAsString):
        char = puzzleFileAsString[fileIndex]
        fileIndex += 1

        # If the current character is a number, add it to the initialState
        if char in includedNums and puzzleIndex < boardHeight * boardLength:
            initialState[puzzleIndex // boardHeight][puzzleIndex % boardLength] = int(char)
            puzzleIndex += 1

    return (Node(state = initialState), fileIndex)




def getInitialNodesFromUserInput():
    initialState = [[0 for _ in range(boardLength)] for _ in range(boardHeight)]

    # --- input 
    print(f"\nInput a puzzle with {boardHeight} rows and {boardLength} columns.")
    print(f"For example, a puzzle with {boardHeight} rows and {boardLength} columns would be inputted like: 0 1 2 3 4 5 6 7 8")
    initialStateString = input("\nInput, then hit enter: ")
    
    # --- collect appropriate numbers for this sized board
    includedNums = set()
    for x in range(boardHeight * boardLength):
        includedNums.add(str(x))

    # --- convert to initial state format 
    index = 0
    for i in range(len(initialStateString)):
        char = initialStateString[i]
        if char in includedNums and index < boardHeight * boardLength:
            initialState[index // boardHeight][index % boardLength] = int(char)
            index += 1
        
    # --- print puzzle for user 
    # print("\nYou inputted:")
    # for row in range(boardHeight):
    #     for col in range(boardLength):
    #         print(initialState[row][col], end=' ')
    #     print("\n")
    
    return Node(state = initialState)
    
    
    
    
    
def puzzleIsSolvable(puzzle):
    print("\nChecking the solvability of the puzzle: ")
    for row in range(boardHeight):
        for col in range(boardLength):
            print(puzzle.state[row][col], end=' ')
        print("")

    # --- Check for number of inversions 
    inversions = 0
    flatPuzzle = [tile for row in puzzle.state for tile in row if tile != 0]
    for i in range(len(flatPuzzle)):
        for j in range(i + 1, len(flatPuzzle)):
            if flatPuzzle[i] > flatPuzzle[j]:
                inversions += 1
    return True if inversions % 2 == 0 else False
    



def getPuzzles(puzzleAmntPref, inputPreference):
    initialPuzzleNodes = []
    numPuzzlesToSolve = 4 # default to multi puzzle test - changes if user decides single 

    # --- adjust number of puzzles to intake based on preference
    if puzzleAmntPref == 1: # single test
        numPuzzlesToSolve = 1
    elif puzzleAmntPref == 3:
        exit() 
    
    # --- select from random gen, file, or manual input 
    i = 0 
    
    while i < numPuzzlesToSolve:
        match inputPreference:
            case 1:
                initialPuzzleNodes.append(getRandomPuzzle())
                # Random puzzle is inherently solvable 
            case 2: 
                initialPuzzleNodes = getInitialPuzzlesFromFiles()
                i = numPuzzlesToSolve # Above function accounts for multi & single tests
                # Check for solvability 
                for puzzle in initialPuzzleNodes:
                    if puzzleIsSolvable(puzzle):
                        print("Puzzle is solvable.")
                    else:
                        print("▊ Puzzle is not solvable. Exiting.")
                        exit(1) 
            case 3: 
                initialPuzzleNodes.append(getInitialNodesFromUserInput())
                # Check for solvability 
                for puzzle in initialPuzzleNodes:
                    if puzzleIsSolvable(puzzle):
                        print("Puzzle is solvable.")
                    else:
                        print("▊ Puzzle is not solvable. Exiting.")
                        exit(1) 
            case _: 
                print("▊ ERROR with the input preference.")
                exit(-1)
        i += 1
        
    return initialPuzzleNodes





# =====================================================================
# =====================================================================
#                               MAIN
# =====================================================================
# =====================================================================
if __name__ == "__main__":

    # --- clear the terminal
    def clear_terminal():
        os.system('cls' if os.name == 'nt' else 'clear')
    clear_terminal()

    # --- Get user preferences
    print("\nHello, welcome to the 8-puzzle problem solver using the A* algorithm.\n")
    puzzleAmntPref, inputPreference, heuristicPreference = gracefullyGetUserPreferences()    
    if puzzleAmntPref == None:
        exit()
        
    #### REMOVE SOLUTION DEPTH 
    
    # --- Get puzzles through different means
    initialPuzzleNodes = getPuzzles(puzzleAmntPref, inputPreference)
    
    for puzzle in initialPuzzleNodes:
        print(puzzle.state)
        
            
    exit(0)
    

        
    # print("------------------------------------------------")
    # print("Cost of algorithm:", AStarHeuristicComparisonWithFile(boardHeight, boardLength))
    # print("------------------------------------------------")
    # # AStarIDSComparisonWithInput()
