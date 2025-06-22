# Carlos Vargas 
# June 21st, 2025

# CS 4200 - Artificial Intelligence
# Professor Daisy Tang 
# California State Polytechnic University - Pomona











# ---------------------------------------------------------------------
#                              globals and imports
# ---------------------------------------------------------------------



import heapq
import random 
import time
import argparse
import os # For clearing the terminal

BOARD_HEIGHT = 3
BOARD_LENGTH = 3
NUM_PUZZLES_TO_SOLVE = 100 # default to multi puzzle test - changes if user decides single 

GOAL_POSITIONS = {i: (i // BOARD_HEIGHT, i % BOARD_LENGTH) for i in range(BOARD_HEIGHT*BOARD_LENGTH)}
    # This calculates the "goal" positions for any tile given 
    # -- used in the manhattan distance function
    
# -- collect allowable numbers for this sized board
ALLOWED_NUMBERS = set()
for x in range(BOARD_HEIGHT * BOARD_LENGTH):
    ALLOWED_NUMBERS.add(str(x))
    # for example, a 3x3 board has numbers [0,1,2,3,4,5,6,7,8]

def parse_args():
    parser = argparse.ArgumentParser(description="8-puzzle A* solver")
    parser.add_argument('--volume', type=str, default="verbose", help="verbose, silent")
    return parser.parse_args()
args = parse_args()
VOLUME = args.volume









# ---------------------------------------------------------------------
#                              node class 
# ---------------------------------------------------------------------




class Node: 
    def __init__(self, state, g=0, hPref = "h1"):
        self.state = state
        self.g = g  # Think about g(n) as the depth of the search, or the number of moves
        self.stateHash = tuple(tuple(row) for row in state)  # Immutable hash for set operations
        self.h1 = numMisplacedTiles(state)
        self.h2 = summedManhattanDistance(state)
        self.emptyPos = self.findEmptyPos()
        self.hPref = hPref

    def f1(self):
        return self.g + self.h1

    def f2(self):
        return self.g + self.h2

    def findEmptyPos(self):
        for row in range(len(self.state)):
            for col in range(len(self.state[0])):
                if self.state[row][col] == 0:
                    return (row, col)
        return None

    # --- For heapq implementation 
    def __lt__(self, other):
        # For heapq comparison - compare by f() value first, then by g value
        if self.hPref == "h1":
            if self.f1() != other.f1():
                return self.f1() < other.f1()
            return self.g > other.g  # Prefer higher g (deeper) for tie-breaking
        else:
            if self.f2() != other.f2():
                return self.f2() < other.f2()
            return self.g > other.g  # Prefer higher g (deeper) for tie-breaking
    
    def __eq__(self, other):
        return self.stateHash == other.stateHash












# ---------------------------------------------------------------------
#                              algorithms
# ---------------------------------------------------------------------





def solveAndPrintAllPuzzles(initialPuzzleNodes, numPuzzlesToSolve):
    h1AveCost = 0
    h2AveCost = 0
    h1AveTime = 0
    h2AveTime = 0
    h1AveDepth = 0
    h2AveDepth = 0
    puzzleNum = 0
    while len(initialPuzzleNodes) > 0:
        # --- Check for solvability and adding to final starting list
        newInitialNode = heapq.heappop(initialPuzzleNodes)
        if not puzzleIsSolvable(newInitialNode):
            print("▊ Removing from list." if VOLUME not in ["silent", "quite"] else "")
        else: 
            # --- Printing 
            if VOLUME not in ["silent", "quite"] :
                print("\n-----------------------------------------------")
                print("SOLVING... ")
            h1Cost, h1Time, h1Depth = AStar8PuzzleAlgorithm(newInitialNode, "h1")
            h2Cost, h2Time, h2Depth = AStar8PuzzleAlgorithm(newInitialNode, "h2")

            if VOLUME not in ["silent", "quite"] :
                print("H1 Search Cost:", h1Cost)
                print("H2 Search Cost:", h2Cost)
                print(f"H1 Time: {1000 * h1Time:.2f} ms")
                print(f"H2 Time: {1000 * h2Time:.2f} ms")
                print("H1 Average Search Depth:", h1Depth)
                print("H2 Average Search Depth:", h2Depth)
                print("-----------------------------------------------\n")

            h1AveCost += h1Cost
            h2AveCost += h2Cost
            h1AveTime += h1Time
            h2AveTime += h2Time
            h1AveDepth += h1Depth
            h2AveDepth += h2Depth
            
            VOLUME == 'quite' and print("Puzzle number:", puzzleNum)
            puzzleNum += 1

    try: 
        if VOLUME == "quite": 
            print("-----------------------------------------------\n")
            print("H1 Average Search Cost:", h1Cost/numPuzzlesToSolve)
            print("H2 Average Search Cost:", h2Cost/numPuzzlesToSolve)
            print(f"H1 Average Time: {1000 * h1Time:.2f} ms"/numPuzzlesToSolve)
            print(f"H2 Average Time: {1000 * h2Time:.2f} ms"/numPuzzlesToSolve)
            print("H1 Average Search Depth:", h1Depth/numPuzzlesToSolve)
            print("H2 Average Search Depth:", h2Depth/numPuzzlesToSolve)
            print("-----------------------------------------------\n")
    except:
        print("\n▊ ERROR")
             
                    
            


"""
A STAR ALGORITHM 
"""
def AStar8PuzzleAlgorithm(initialNode, heuristicPref):
    SearchCost = 0
    Time = time.process_time()
    steps = 0
    goalState = ((0,1,2),(3,4,5),(6,7,8)) # NEED TO MAKE THIS DYNAMIC
    exploredNodes = set()

    # --- Initialize the frontier as a priority queue
    frontier = []
    heapq.heappush(frontier, initialNode)
    frontierStates = {initialNode.stateHash: initialNode}   # For quicker searcher; we
                                                            # use hashes. This makes
                                                            # storage more cost effective
                                                            # and search decreases. 
    # --- Explore the frontier while there's still nodes 
    while frontier: 
        steps += 1
        currentNode = heapq.heappop(frontier)
        if currentNode.stateHash in frontierStates:
            del frontierStates[currentNode.stateHash]

        # --- printing 
        if steps <= 10 and heuristicPref == "h2" and VOLUME not in ["silent", "quite"] : 
            print("Showing first ten steps: ", end="")
            print(steps)
            printBoard(currentNode.state)
        elif steps == 11 and heuristicPref == "h2" and VOLUME not in ["silent", "quite"] :
            print("...")
        # if heuristicPref == "h2" and VOLUME not in ["silent", "quite"] : 
        #     print("Steps:", steps)
        # print("▊ Current Depth:", currentNode.g if VOLUME not in ["silent", "quite"] else "" )
        
        # --- Checking against the solution
        if currentNode.stateHash == goalState:
            Time = time.process_time() - Time
            return (SearchCost, Time, currentNode.g)
        
        exploredNodes.add(currentNode.stateHash)
        successorNodes = findSuccessorNodes(currentNode, heuristicPref)

        # --- Exploring each successor node
        for successorNode in successorNodes:
            successorHash = successorNode.stateHash
            
            if successorHash in exploredNodes:  # Check if it's in the explored list
                continue
            if successorHash in frontierStates:     # Check if it's in the frontier list
                existingNode = frontierStates[successorHash]
                if successorNode.g < existingNode.g:
                    existingNode.g = float('inf')  # Mark as invalid
                    heapq.heappush(frontier, successorNode)
                    SearchCost += 1
                    frontierStates[successorHash] = successorNode
            else:  # --- Add it to the frontier list
                heapq.heappush(frontier, successorNode)
                SearchCost += 1
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





def numMisplacedTiles(state):
    flatState = [tile for row in state for tile in row if tile != 0]
    numMisplacedTiles = 0
    for i in range(len(flatState)):
        if i != flatState[i]:
            numMisplacedTiles += 1
    return numMisplacedTiles

    

    
'''
@Input: currentNode = [BOARD_LENGTH X BOARD_HEIGHT]
@Input: BOARD_LENGTH
@Input: BOARD_HEIGHT
'''
def findSuccessorNodes(currentNode, heuristicPref):
    successors = []
    state = currentNode.state

    # --- Find empty position
    emptyPos = currentNode.emptyPos
    row, col = emptyPos

    moves = [(-1, 0), (1, 0), (0, 1), (0, -1)] # The possibility of moves up down right left
    
    for directionalOffsetRow, directionalOffsetCol in moves:
        newRow, newCol = row + directionalOffsetRow, col + directionalOffsetCol
        
        if 0 <= newRow < BOARD_HEIGHT and 0 <= newCol < BOARD_LENGTH: # Check bounds
            # Create new state by swapping
            newState = [list(row) for row in state]  # Deep copy
            newState[row][col], newState[newRow][newCol] = newState[newRow][newCol], newState[row][col]
            
            # Create new node
            newNode = Node(state=newState, g=currentNode.g + 1, hPref=heuristicPref)
            successors.append(newNode)

    return successors














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
        userHeuristicPreference = input(
            "\nSelect H Function:\n"
            "[1] H1\n"
            "[2] H2\n"
            "Your choice: "
        )
        # ---- Handle errors with input
        try:
            userHeuristicPreference = int(userHeuristicPreference)
            if (1 > userHeuristicPreference or userHeuristicPreference > 2):
                invalidInput = True
                print("\n▊ ERROR: Please only input an integer (1 or 2) followed by a return")
            else:
                invalidInput = False
        except:
            print("\n▊ ERROR: Please only input an integer (1 or 2) followed by a return")
    
    return [puzzleAmntPref, inputPreference, userHeuristicPreference]




"""
Generate a random puzzle with integers between 0 and BOARD_LENGTH * BOARD_HEIGHT inclusive 
"""
def getRandomPuzzle():
    puzzle = [[0 for _ in range(BOARD_LENGTH)] for _ in range(BOARD_HEIGHT)]
        
    listOfNums = []
    for i in range(BOARD_HEIGHT*BOARD_LENGTH):
        listOfNums.append(i)
    random.shuffle(listOfNums)
    
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_LENGTH):
            puzzle[row][col] = listOfNums[0]
            listOfNums.remove(listOfNums[0])
    
    # --- print puzzle for testing
    # for row in range(BOARD_HEIGHT):
    #     for col in range(BOARD_LENGTH):
    #         print(puzzle[row][col], end=' ')
    #     print("\n")
    
    return Node(state = puzzle)

   
   
    
def getInitialPuzzlesFromFiles():
    filename = input("\nEnter the destination of the file containing ALL the puzzles to be solved: ")
    initialPuzzleNodes = []
    
    # read file - handle errors 
    puzzleFileAsString = ""
    try: 
        with open(filename, 'r') as file:
            puzzleFileAsString = file.read()
    except:
        print("\n▊ Can't find that file. Exiting.\n")
        exit(1)
    
    # While there is still a puzzle to be read from the file
    fileIndex = 0
    while fileIndex < len(puzzleFileAsString):
        initialNode, fileIndex = getNextPuzzleFromFileString(puzzleFileAsString, BOARD_HEIGHT, BOARD_LENGTH, fileIndex)
        # initialPuzzleNodes.append(initialNode)
        heapq.heappush(initialPuzzleNodes, initialNode)

    return initialPuzzleNodes

    


def getNextPuzzleFromFileString(puzzleFileAsString, BOARD_HEIGHT, BOARD_LENGTH, fileIndex):
    initialState = [[0 for _ in range(BOARD_LENGTH)] for _ in range(BOARD_HEIGHT)]
    puzzleIndex = 0
    
    # Fill out the initialState with the given numbers from next puzzle
    while puzzleIndex < BOARD_HEIGHT * BOARD_LENGTH and fileIndex < len(puzzleFileAsString):
        char = puzzleFileAsString[fileIndex]
        fileIndex += 1

        # If the current character is a number, add it to the initialState
        if char in ALLOWED_NUMBERS and puzzleIndex < BOARD_HEIGHT * BOARD_LENGTH:
            initialState[puzzleIndex // BOARD_HEIGHT][puzzleIndex % BOARD_LENGTH] = int(char)
            puzzleIndex += 1

    return (Node(state = initialState), fileIndex)




def getInitialPuzzleFromUserInput():
    initialState = [[0 for _ in range(BOARD_LENGTH)] for _ in range(BOARD_HEIGHT)]

    # --- input 
    print(f"\nInput a puzzle with {BOARD_HEIGHT} rows and {BOARD_LENGTH} columns.")
    print(f"For example, a puzzle with 3 rows and 3 columns would be inputted like: 0 1 2 3 4 5 6 7 8")
    initialStateString = input("\nInput, then hit enter: ")
    
    # --- convert to initial state format 
    index = 0
    for i in range(len(initialStateString)):
        char = initialStateString[i]
        if char in ALLOWED_NUMBERS and index < BOARD_HEIGHT * BOARD_LENGTH:
            initialState[index // BOARD_HEIGHT][index % BOARD_LENGTH] = int(char)
            index += 1
        
    # --- print puzzle for user 
    # print("\nYou inputted:")
    # for row in range(BOARD_HEIGHT):
    #     for col in range(BOARD_LENGTH):
    #         print(initialState[row][col], end=' ')
    #     print("\n")
    
    return Node(state = initialState)
    
    
    
    
def getPuzzles(puzzleAmntPref, inputPreference, numPuzzlesToSolve):
    initialPuzzleNodes = []
    
    # --- adjust number of puzzles to intake based on preference
    if puzzleAmntPref == 1: # single test
        numPuzzlesToSolve = 1
    elif puzzleAmntPref == 3:
        exit() 
    
    # --- select from random gen, file, or manual input 
    i = 0 
    
    while i < numPuzzlesToSolve:  # repeat for multiple puzzles 
        match inputPreference:
            case 1:
                heapq.heappush(initialPuzzleNodes, getRandomPuzzle())
                # Random puzzle is inherently solvable 
            case 2: 
                initialPuzzleNodes = getInitialPuzzlesFromFiles()
                i = numPuzzlesToSolve # Above function accounts for multi & single tests
            case 3: 
                heapq.heappush(initialPuzzleNodes, getInitialPuzzleFromUserInput())
            case _: 
                print("▊ ERROR with the input preference.")
                exit(-1)
        i += 1

    return initialPuzzleNodes





"""
Checks for inversions as well as unfilled puzzles. 
Unfilled puzzles are puzzles that are similar to this: 
4 5 6
0 0 0 
0 0 0
This would not get picked up as unsolvable with inversions.
"""    
def puzzleIsSolvable(puzzle):
    print("\nChecking the solvability of the puzzle: " if VOLUME not in ["silent", "quite"] else "")

    # --- Check for unfilled puzzles (print at same time)
    items = set() 
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_LENGTH):
            items.add(puzzle.state[row][col])

    if len(items) < BOARD_HEIGHT*BOARD_LENGTH:
        print("▊ Puzzle is not solvable." if VOLUME not in ["silent", "quite"] else "")
        return False
    
    # --- Check for number of inversions 
    inversions = 0
    flatPuzzle = [tile for row in puzzle.state for tile in row if tile != 0]
    for i in range(len(flatPuzzle)):
        for j in range(i + 1, len(flatPuzzle)):
            if flatPuzzle[i] > flatPuzzle[j]:
                inversions += 1
                
    if inversions % 2 == 0:
        print("Puzzle is solvable." if VOLUME not in ["silent", "quite"] else "")
        return True
    else:
        print("▊ Puzzle is not solvable." if VOLUME not in ["silent", "quite"] else "")
        return False
    






def printBoard(state):
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_LENGTH):
            print(state[row][col], end=' ')
        print("")
    print("")
    














# ====================================================================================
# ====================================================================================
#                                  MAIN
# ====================================================================================
# ====================================================================================
if __name__ == "__main__":
    numPuzzlesToSolve = NUM_PUZZLES_TO_SOLVE

    # --------- clear the terminal
    def clear_terminal():
        os.system('cls' if os.name == 'nt' else 'clear')
    clear_terminal()

    # --------- Get user preferences
    print("\nHello, welcome to the 8-puzzle problem solver using the A* algorithm.\n")
    puzzleAmntPref, inputPreference, userHeuristicPreference = gracefullyGetUserPreferences()    
    if puzzleAmntPref == None: 
        # the user chose to exit
        exit(0)
        
    # --------- Get puzzles through different means
    initialPuzzleNodes = getPuzzles(puzzleAmntPref, inputPreference, numPuzzlesToSolve)
    
    # --------- Solving the puzzles 
    solveAndPrintAllPuzzles(initialPuzzleNodes, numPuzzlesToSolve)
            
    exit(0)
