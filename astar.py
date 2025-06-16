# Carlos Vargas 
# June 21st, 2025

# CS 4200 - Artificial Intelligence
# Professor Daisy Tang 
# California State Polytechnic University - Pomona

# -----------------------------------------------------------------




def AStar8PuzzleAlgorithm(initialNode, boardHeight, boardLength):
    goalState = [[0,1,2],[3,4,5],[6,7,8]]
    exploredNodes = []
    # depthLevel = 0 # This can also be thought of as the cost to get to node n

    # Initialize the cost of the root node
    currentNodeGCost = 0
    currentNodeHCost = summedManhattanDistance(initialNode.state)
    currentNodeFCost = currentNodeGCost + currentNodeHCost

    # Initialize the frontier as a priority queue (see sortPriorityQueueByFn())
    frontier = []
    frontier.append(initialNode) # Initial node 

    # Explore the frontier while there's still nodes 
    while len(frontier) > 0: 
        currentNode = frontier[0]
        if currentNode.state == goalState:
            return currentNode.g 
        
        # Get a priority queue of the successor nodes, ordered by lowest HEURISTIC cost
        successorNodes = findSuccessorNodes(currentNode, boardLength, boardHeight)

        # Exploring each successor node
        while len(successorNodes) > 0:
            successorNode = Node(successorNodes[0].state)
            successorNode.g = currentNode.g + 1
            successorNodes.pop(0)
            
            # Determine what to do with the successor 
            if inPriorityQueue(successorNode.state, frontier) != -1:    # Check if it's in the frontier list
                indexOfExistingNode = inPriorityQueue(successorNode.state, frontier)
                if successorNode.f() > frontier[indexOfExistingNode[0]]: continue
            elif inPriorityQueue(successorNode.state, exploredNodes) != -1:   # Check if it's in the explored list
                indexOfExistingNode = inPriorityQueue(successorNode.state, frontier)
                if successorNode.f() > frontier[indexOfExistingNode[0]]: continue
                moveItemBetweenQueues(successorNode, exploredNodes, frontier) 
            else:                                                       # Add it to the frontier list
                frontier.append(successorNode)
                frontier = sortPriorityQueueByFn(frontier)

        moveItemBetweenQueues(currentNode, frontier, exploredNodes)
    
    if currentNode.state != goalState: return "ERROR"




"""
Move item from priority queue 1 to priority queue 2
"""
def moveItemBetweenQueues(item, q1, q2):
    q1.remove(item)
    q2.append(item)
    q2 = sortPriorityQueueByFn(q2)


"""
This determines if a state is in a priority queue regardless of the priority value.
@Output: The index of the matching state within the priority queue.
@Output: -1 if it is not within the priority queue.
"""
def inPriorityQueue(goalState, priorityQ):
    # for row in range(len(priorityQ)):
    if goalState in priorityQ:
        return True
    else: return -1



'''
@Input: originalNode = [boardLength X boardHeight]
@Input: boardLength
@Input: boardHeight
@Output: deep copy of originalNode
'''
def deepCopy(originalNode, boardLength, boardHeight):
    copyNode = Node(state = [[0 for _ in range(boardLength)] for _ in range(boardHeight)])
    for row in range(boardHeight):
        for column in range(boardLength):
            copyNode.state[row][column] = originalNode.state[row][column]
    copyNode.g = originalNode.g
    return copyNode




def sortPriorityQueueByFn(priorityQ):
    for node in range(len(priorityQ)):
        for j in range(0, len(priorityQ) - node - 1):
            if priorityQ[j].f() > priorityQ[j + 1].f():
                priorityQ[j], priorityQ[j + 1] = priorityQ[j + 1], priorityQ[j]
    return priorityQ




'''
@Input: exampleNode = [[0,1,2],[3,4,5],[6,7,8]], where the rows and columns can vary
@Output: integer sum of the manhattan distances 
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




def swapTiles(tile1Index, tile2Index, node):
    swappableTile = node.state[tile1Index[0]][tile1Index[1]]
    node.state[tile1Index[0]][tile1Index[1]] = node.state[tile2Index[0]][tile2Index[1]]
    node.state[tile2Index[0]][tile2Index[1]] = swappableTile


'''
@Input: currentNode = [boardLength X boardHeight]
@Input: boardLength
@Input: boardHeight
'''
def findSuccessorNodes(currentNode, boardLength, boardHeight):
    indexOfEmptySpace = [None, None] 
    listOfSuccessorNodes = []

    # Find the index of the empty tile, 0
    for row in range(boardHeight):
        try:
            indexOfEmptySpace = [row, currentNode.state[row].index(0)]
            break
        except ValueError:
            pass 

    if indexOfEmptySpace[0] > 0: # check if empty space can be swapped with above tile, then swap
        nextNode = deepCopy(currentNode, boardLength, boardHeight)
        swapTiles([indexOfEmptySpace[0]-1, indexOfEmptySpace[1]], [indexOfEmptySpace[0], indexOfEmptySpace[1]], nextNode)
        listOfSuccessorNodes.append(nextNode)

    if indexOfEmptySpace[0] < boardHeight-1: # check if empty space can be swapped with below tile, then swap
        nextNode = deepCopy(currentNode, boardLength, boardHeight)
        swapTiles([indexOfEmptySpace[0]+1, indexOfEmptySpace[1]], [indexOfEmptySpace[0], indexOfEmptySpace[1]], nextNode)
        listOfSuccessorNodes.append(nextNode)

    if indexOfEmptySpace[1] < boardLength-1: # check if empty space can be swapped with right-adjacent tile, then swap
        nextNode = deepCopy(currentNode, boardLength, boardHeight)
        swapTiles([indexOfEmptySpace[0], indexOfEmptySpace[1]+1], [indexOfEmptySpace[0], indexOfEmptySpace[1]], nextNode)
        listOfSuccessorNodes.append(nextNode)

    if indexOfEmptySpace[1] > 0: # check if empty space can be swapped with left-adjacent tile, then swap
        nextNode = deepCopy(currentNode, boardLength, boardHeight)
        swapTiles([indexOfEmptySpace[0], indexOfEmptySpace[1]-1], [indexOfEmptySpace[0], indexOfEmptySpace[1]], nextNode)
        listOfSuccessorNodes.append(nextNode)

    return sortPriorityQueueByFn(listOfSuccessorNodes)




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




class Node: 
    def __init__(self, state, g=0):
        self.state = state
        self.g = g     # Think about g(n) as the depth of the search, or the number of moves
    def h(self):
        return summedManhattanDistance(self.state)
    def f(self):
        return self.g + self.h()




# =====================================================================
#                               MAIN
# =====================================================================
if __name__ == "__main__":

    print("------------------------------------------------")
    initialNode = Node(state = [[1,2,3],[0,4,5],[6,7,8]])
    print("Cost of algorithm:",AStar8PuzzleAlgorithm(initialNode, 3, 3))
    # print("Cost of algorithm:",AStarIDSComparisonWithFile())
    print("------------------------------------------------")
    # AStarIDSComparisonWithInput()





# def manhattanDistance(state, goalState):
#     goalState = int(goalState)
#     horizontalDistance = abs(state % 3 - goalState % 3)
#     verticalDistance = abs(int(state / 3) - int(goalState / 3))
#     return verticalDistance + horizontalDistance

