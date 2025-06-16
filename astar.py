# Carlos Vargas 
# June 21st, 2025

# CS 4200 - Artificial Intelligence
# Professor Daisy Tang 
# California State Polytechnic University - Pomona

# -----------------------------------------------------------------

def AStar8PuzzleAlgorithm(initialNode, boardHeight, boardLength):
    goalState = [[0,1,2],[3,4,5],[6,7,8]]
    exploredNodes = []
    depthLevel = 0 # This can also be thought of as the cost to get to node n

    # Initialize the cost of the root node
    currentNodeGCost = 0
    currentNodeHCost = summedManhattanDistance(initialNode)
    currentNodeFCost = currentNodeGCost + currentNodeHCost

    # Initialize the frontier as a priority queue
    frontier = []
    frontier.append((currentNodeFCost, initialNode)) # Initial node 

    # Explore the frontier while there's still nodes 
    while len(frontier) > 0: 
        currentNode = frontier[0]

        if currentNode[1] == goalState:
            return currentNode[0]
        
        # Get a priority queue of the successor nodes, ordered by lowest HEURISTIC cost
        successorNodes = findSuccessorNodes(currentNode[1], boardLength, boardHeight)
        # print("▊", successorNodes)
        depthLevel += 1 

        # Initialize the cost of current successor node
        successorNodeGCost = depthLevel
        successorNodeHCost = summedManhattanDistance(currentNode[1])
        successorNodeFCost = successorNodeGCost + successorNodeHCost

        # Exploring each successor node
        while len(successorNodes) > 0:
            successorNode = (successorNodes[0][0] + 1, successorNodes[0][1])    # This makes the
            successorNodes.pop(0)                                               # cost of the 
                                                                                # successor:
                                                                                # g(n) + h(n), where g(n)=1
            if successorNode in frontier:
                if successorNodeGCost <= successorNode[0]: continue
            elif successorNode in exploredNodes: 
                if successorNodeGCost <= successorNode[0]: continue
                frontier.append(successorNode)    # Move successor from explored to frontier
                frontier = sorted(frontier)
                exploredNodes.remove(successorNode)
            else: 
                frontier.append(successorNode)
                frontier = sorted(frontier)
            successorNodeGCost = successorNode[0]

        exploredNodes.append(frontier.pop(0))   # Move current node to the explored list 
        exploredNodes = sorted(exploredNodes)
    
    if currentNode[1] != goalState: return "ERROR"




'''
@Input: originalNode = [boardLength X boardHeight]
@Input: boardLength
@Input: boardHeight
@Output: deep copy of originalNode
'''
def deepCopy(originalNode, boardLength, boardHeight):
    copyNode = [[0 for _ in range(boardLength)] for _ in range(boardHeight)]
    for row in range(boardHeight):
        for column in range(boardLength):
            copyNode[row][column] = originalNode[row][column]
    return copyNode




# def manhattanDistance(state, goalState):
#     goalState = int(goalState)
#     horizontalDistance = abs(state % 3 - goalState % 3)
#     verticalDistance = abs(int(state / 3) - int(goalState / 3))
#     return verticalDistance + horizontalDistance




'''
@Input: exampleNode = [[0,1,2],[3,4,5],[6,7,8]], where the rows and columns can vary
@Outpute: integer sum of the manhattan distances 
'''
def summedManhattanDistance(node): 
    lengthOfBoard = len(node[0])
    heightOfBoard = len(node)
    sumOfDistances = 0 
    for row in range(heightOfBoard):
        for column in range(lengthOfBoard):
            tileFaceValue = node[row][column]
            horizontalDistance = abs(tileFaceValue % lengthOfBoard - column )
            verticalDistance = abs(int(tileFaceValue / heightOfBoard) - row)
            sumOfDistances += verticalDistance + horizontalDistance
    # print(▊ sumOfDistances)
    return sumOfDistances




'''
@Input: currentNode = [boardLength X boardHeight]
@Input: boardLength
@Input: boardHeight
'''
def findSuccessorNodes(currentNode, boardLength, boardHeight):
    indexOfEmptySpace = [None, None] 
    listOfSuccessorNodes = []

    # Find the index of the empty tile, 0
    for row in range(len(currentNode)):
        try:
            indexOfEmptySpace = [row, currentNode[row].index(0)]
            break
        except ValueError:
            pass 

    # check if empty space can be swapped with above tile, then swap
    if indexOfEmptySpace[0] > 0: 
        # print("▊ Swap up")
        nextNode = deepCopy(currentNode, boardLength, boardHeight)
        swappableTile = nextNode[indexOfEmptySpace[0] - 1][indexOfEmptySpace[1]]
        nextNode[indexOfEmptySpace[0] - 1][indexOfEmptySpace[1]] = nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1]]
        nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1]] = swappableTile
        listOfSuccessorNodes.append((summedManhattanDistance(nextNode), nextNode))
        print("▊ Next node: ", nextNode)
    # check if empty space can be swapped with below tile, then swap
    if indexOfEmptySpace[0] < boardHeight - 1:
        # print("▊ Swap down")
        nextNode = deepCopy(currentNode, boardLength, boardHeight)
        swappableTile = nextNode[indexOfEmptySpace[0] + 1][indexOfEmptySpace[1]]
        nextNode[indexOfEmptySpace[0] + 1][indexOfEmptySpace[1]] = nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1]]
        nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1]] = swappableTile
        listOfSuccessorNodes.append((summedManhattanDistance(nextNode), nextNode))
        print("▊ Next node: ", nextNode)
    # check if empty space can be swapped with right-adjacent tile, then swap
    if indexOfEmptySpace[1] < boardLength - 1: 
        # print("▊ Swap right")
        nextNode = deepCopy(currentNode, boardLength, boardHeight)
        swappableTile = nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1] + 1]
        nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1] + 1] = nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1]]
        nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1]] = swappableTile
        listOfSuccessorNodes.append((summedManhattanDistance(nextNode), nextNode))
        print("▊ Next node: ", nextNode)
    # check if empty space can be swapped with left-adjacent tile, then swap
    if indexOfEmptySpace[1] > 0: 
        # print("▊ Swap left")
        nextNode = deepCopy(currentNode, boardLength, boardHeight)
        swappableTile = nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1] - 1]
        nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1] - 1] = nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1]]
        nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1]] = swappableTile
        listOfSuccessorNodes.append((summedManhattanDistance(nextNode), nextNode))
        print("▊ Next node: ", nextNode)

    return sorted(listOfSuccessorNodes)




def getNextInitialPuzzle(puzzleIndex, puzzleDatabaseFile, boardHeight, boardLength, puzzleFileIndex):
    initialNode = [[0 for _ in range(boardLength)] for _ in range(boardHeight)]

    # Fill out the initialNode with the given numbers from next puzzle
    while puzzleIndex < boardHeight * boardLength: 
        char = puzzleDatabaseFile[puzzleFileIndex]
        puzzleFileIndex += 1

        # If the current character is a number, add it to the initialNode
        if char in '012345678' and puzzleIndex < boardHeight * boardLength:
            initialNode[int(puzzleIndex / boardHeight)][puzzleIndex % boardLength] = int(char)
            puzzleIndex += 1

    return (initialNode, puzzleFileIndex)




def AStarIDSComparisonWithFile():
    # initialize board 
    boardLength = 3
    boardHeight = 3

    # read file 
    puzzleDatabaseFile = ""
    with open('project-1-instructions/Length4-2.txt', 'r') as file:
        puzzleDatabaseFile = file.read()


    # While there is still a puzzle to be worked on: 
    puzzleFileIndex = 0
    while puzzleFileIndex < len(puzzleDatabaseFile):
        indexAndPuzzleTuple = getNextInitialPuzzle(0, puzzleDatabaseFile, boardHeight, boardLength, puzzleFileIndex)
        puzzleFileIndex = indexAndPuzzleTuple[1]

        return AStar8PuzzleAlgorithm(indexAndPuzzleTuple[0], boardHeight, boardLength)



            




# =====================================================================
#                               MAIN
# =====================================================================
if __name__ == "__main__":

    AStarIDSComparisonWithFile()
    # AStarIDSComparisonWithInput()