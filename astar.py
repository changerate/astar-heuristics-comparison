# Carlos Vargas 
# June 14th, 2025

# CS 4200 - Artificial Intelligence
# Professor Daisy Tang 
# California State Polytechnic University - Pomona

# -----------------------------------------------------------------


import heapq




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
@Input: exampleNode = [[0,1,2],[3,4,5],[6,7,8]]
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


def findSuccessorNodes(currentNode, boardLength, boardHeight):
    indexOfEmptySpace = [None, None] 
    listOfSuccessorNodes = []

    # Find the index of the empty tile, 0
    for row in range(len(currentNode)):
        try:
            indexOfEmptySpace = [currentNode[row].index(0), row]
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
        heapq.heappush(listOfSuccessorNodes, (summedManhattanDistance(nextNode), nextNode))
        print("▊ Next node: ", nextNode)
    # check if empty space can be swapped with below tile, then swap
    if indexOfEmptySpace[0] < boardHeight - 1:
        # print("▊ Swap down")
        nextNode = deepCopy(currentNode, boardLength, boardHeight)
        swappableTile = nextNode[indexOfEmptySpace[0] + 1][indexOfEmptySpace[1]]
        nextNode[indexOfEmptySpace[0] + 1][indexOfEmptySpace[1]] = nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1]]
        nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1]] = swappableTile
        heapq.heappush(listOfSuccessorNodes, (summedManhattanDistance(nextNode), nextNode))
        print("▊ Next node: ", nextNode)
    # check if empty space can be swapped with right-adjacent tile, then swap
    if indexOfEmptySpace[1] < boardLength - 1: 
        # print("▊ Swap right")
        nextNode = deepCopy(currentNode, boardLength, boardHeight)
        swappableTile = nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1] + 1]
        nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1] + 1] = nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1]]
        nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1]] = swappableTile
        heapq.heappush(listOfSuccessorNodes, (summedManhattanDistance(nextNode), nextNode))
        print("▊ Next node: ", nextNode)
    # check if empty space can be swapped with left-adjacent tile, then swap
    if indexOfEmptySpace[1] > 0: 
        # print("▊ Swap left")
        nextNode = deepCopy(currentNode, boardLength, boardHeight)
        swappableTile = nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1] - 1]
        nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1] - 1] = nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1]]
        nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1]] = swappableTile
        heapq.heappush(listOfSuccessorNodes, (summedManhattanDistance(nextNode), nextNode))
        print("▊ Next node: ", nextNode)

    return listOfSuccessorNodes




def nodeInPriorityQueue(goalNode, priorityQueue):
    for node in range(len(priorityQueue)): 
        if (goalNode in priorityQueue[node]):
            return True
    else: return False 





def AStarIDSComparisonWithFile():
    # initialize board 
    goalState = [[0,1,2],[3,4,5],[6,7,8]]
    boardLength = 3
    boardHeight = 3
    initialNode = [[0 for _ in range(boardLength)] for _ in range(boardHeight)]

    # read file 
    puzzleDatabaseFile = ""
    with open('project-1-instructions/Length4-2.txt', 'r') as file:
    # with open('project-1-instructions/Length4-1.txt', 'r') as file:
    # with open('project-1-instructions/Length4.txt', 'r') as file:
        puzzleDatabaseFile = file.read()




    # While there is still a puzzle to be worked on: 
    charIndex = 0
    while charIndex < len(puzzleDatabaseFile):
        puzzleIndex = 0

        # Fill out the initialNode with the given numbers from one puzzle
        while puzzleIndex < boardHeight * boardLength: 
            char = puzzleDatabaseFile[charIndex]
            charIndex += 1

            # If the current character is a number, add it to the initialNode
            if char in '012345678' and puzzleIndex < boardHeight * boardLength:
                initialNode[int(puzzleIndex / boardHeight)][puzzleIndex % boardLength] = int(char)
                puzzleIndex += 1


        #==================================
        #  A-Star (A*) Program
        #==================================
        exploredNodes = []
        heuristicCost = summedManhattanDistance(initialNode)
        currentCost = 0
        # currentTotalCost = currentCost + heuristicCost
        depthLevel = 0 # This can also be thought of as the cost to get to node n
        frontierQ = []
        heapq.heappush(frontierQ, (summedManhattanDistance(initialNode), initialNode)) # Initial node

        while len(frontierQ) > 0: 
            currentNode = frontierQ[0][1]
            # currentTotalCost = depthLevel + summedManhattanDistance(currentNode)
            if currentNode == goalState:
                return currentCost
            
            # Get a priority queue of the successor nodes, ordered by lowest heuristic cost
            successorNodes = findSuccessorNodes(currentNode, boardLength, boardHeight)
            # print("▊", successorNodes)
            depthLevel += 1 

            # Exploring each successor node
            while len(successorNodes) > 0:
                successorTotalCost = successorNodes[0][0] + 1   # The cost to get to the next state is always
                                                                # just +1 because tiles can only move 1 step 
                                                                # at a time.
                                                                # The index [0][0] signifies the heuristic
                                                                # cost of the highest priority node. 
                successorNode = heapq.heappop(successorNodes)
                successorNode = successorNode[1]    # We pop it from the queue, then assign the actual
                                                    # node to the successor node. 
                # check if this successor is already in the frontier 
                if nodeInPriorityQueue(successorNode, frontierQ): 
                    if depthLevel <= successorTotalCost: continue
                elif successorNode in exploredNodes: 
                    if depthLevel <= successorTotalCost: continue
                    heapq.heappush(frontierQ, (successorTotalCost, exploredNodes.pop(successorNode)))
                else: 
                    heapq.heappush(frontierQ, (successorTotalCost, successorNode))

            exploredNodes.append(currentNode)
        
        if currentNode != goalState: return "ERROR"

            




# =====================================================================
#                               MAIN
# =====================================================================
if __name__ == "__main__":

    AStarIDSComparisonWithFile()
    # AStarIDSComparisonWithInput()