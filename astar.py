# Carlos Vargas 
# June 21st, 2025

# CS 4200 - Artificial Intelligence
# Professor Daisy Tang 
# California State Polytechnic University - Pomona

# -----------------------------------------------------------------

import copy 




def AStar8PuzzleAlgorithm(initialNode, boardHeight, boardLength):
    goalState = [[0,1,2],[3,4,5],[6,7,8]]
    exploredNodes = []

    # Initialize the frontier as a priority queue (see sortPriorityQueueByFn())
    frontier = []
    frontier.append(initialNode) # Initial node 

    # Explore the frontier while there's still nodes 
    while len(frontier) > 0: 
        currentNode = frontier[0]
        # print("▊", currentNode.state)
        print("▊ Current Depth:", currentNode.g)
        
        if currentNode.state == goalState:
            return currentNode.g 
        
        # Get a priority queue of the successor nodes, ordered by lowest HEURISTIC cost
        successorNodes = findSuccessorNodes(currentNode, boardLength, boardHeight)

        # Exploring each successor node
        while len(successorNodes) > 0:
            successorNode = successorNodes[0]
            successorNodes.pop(0)
            
            # Determine what to do with the successor 
            if successorNode in frontier:                   # Check if it's in the frontier list
                if successorNode.f() > frontier[frontier.index(successorNode)]: continue
            elif successorNode in exploredNodes:            # Check if it's in the explored list
                if successorNode.f() > exploredNodes[exploredNodes.index(successorNode)]: continue
                moveItemBetweenQueues(successorNode, exploredNodes, frontier) 
            else:                                           # Add it to the frontier list
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
            goalRow, goalCol = GOAL_POSITIONS[tileFaceValue]
            sumOfDistances += abs(row - goalRow) + abs(column - goalCol)
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
    successors = []

    for row in range(len(currentNode.state)):
        for col in range(len(currentNode.state[0])):
            if currentNode.state[row][col] == 0:
                emptyPos = (row, col)

    if emptyPos[0] > 0: # check if empty space can be swapped with above tile, then swap
        nextNode = copy.deepcopy(currentNode)
        swapTiles([emptyPos[0]-1, emptyPos[1]], [emptyPos[0], emptyPos[1]], nextNode)
        nextNode.g += 1
        successors.append(nextNode)

    if emptyPos[0] < boardHeight-1: # check if empty space can be swapped with below tile, then swap
        nextNode = copy.deepcopy(currentNode)
        swapTiles([emptyPos[0]+1, emptyPos[1]], [emptyPos[0], emptyPos[1]], nextNode)
        nextNode.g += 1
        successors.append(nextNode)

    if emptyPos[1] < boardLength-1: # check if empty space can be swapped with right-adjacent tile, then swap
        nextNode = copy.deepcopy(currentNode)
        swapTiles([emptyPos[0], emptyPos[1]+1], [emptyPos[0], emptyPos[1]], nextNode)
        nextNode.g += 1
        successors.append(nextNode)

    if emptyPos[1] > 0: # check if empty space can be swapped with left-adjacent tile, then swap
        nextNode = copy.deepcopy(currentNode)
        swapTiles([emptyPos[0], emptyPos[1]-1], [emptyPos[0], emptyPos[1]], nextNode)
        nextNode.g += 1
        successors.append(nextNode)

    return sortPriorityQueueByFn(successors)




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
    listOfCosts = [] 

    # read file 
    puzzleDatabaseFile = ""
    with open('project-1-instructions/Length4.txt', 'r') as file:
        puzzleDatabaseFile = file.read()


    # While there is still a puzzle to be worked on: 
    puzzleFileIndex = 0
    while puzzleFileIndex < len(puzzleDatabaseFile):
        indexAndPuzzleTuple = getNextInitialPuzzle(0, puzzleDatabaseFile, boardHeight, boardLength, puzzleFileIndex)
        puzzleFileIndex = indexAndPuzzleTuple[1]

        initialNode = Node(state = indexAndPuzzleTuple[0])
        listOfCosts.append(AStar8PuzzleAlgorithm(initialNode, boardHeight, boardLength))

    return listOfCosts




class Node: 
    def __init__(self, state, g=0):
        self.state = state
        self.g = g     # Think about g(n) as the depth of the search, or the number of moves
        self.h = summedManhattanDistance(state)
    #     self.emptyPos = self._findEmptyPos()

    # def _findEmptyPos(self):
    #     for row in range(len(self.state)):
    #         for col in range(len(self.state[0])):
    #             if self.state[row][col] == 0:
    #                 return (row, col)
    #     return None
            
    def f(self):
        return self.g + self.h



# =====================================================================
#                               MAIN
# =====================================================================
if __name__ == "__main__":

    GOAL_POSITIONS = {i: (i//3, i%3) for i in range(9)}

    print("------------------------------------------------")
    initialNode = Node(state = [[1,2,3],[0,4,5],[6,7,8]]) # NO SOLUTION!! 😤
    initialNode = Node(state = [[1,2,5],[3,4,8],[6,7,0]])


    # print("Cost of algorithm:", AStar8PuzzleAlgorithm(initialNode, 3, 3))
    print("Cost of algorithm:", AStarIDSComparisonWithFile())
    print("------------------------------------------------")
    # AStarIDSComparisonWithInput()
