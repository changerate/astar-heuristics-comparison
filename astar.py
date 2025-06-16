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
        listOfSuccessorNodes.append(nextNode)
        # print("▊ Next node: ", nextNode)
    # check if empty space can be swapped with below tile, then swap
    if indexOfEmptySpace[0] < boardHeight - 1:
        # print("▊ Swap down")
        nextNode = deepCopy(currentNode, boardLength, boardHeight)
        swappableTile = nextNode[indexOfEmptySpace[0] + 1][indexOfEmptySpace[1]]
        nextNode[indexOfEmptySpace[0] + 1][indexOfEmptySpace[1]] = nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1]]
        nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1]] = swappableTile
        listOfSuccessorNodes.append(nextNode)
        # print("▊ Next node: ", nextNode)
    # check if empty space can be swapped with right-adjacent tile, then swap
    if indexOfEmptySpace[1] < boardLength - 1: 
        # print("▊ Swap right")
        nextNode = deepCopy(currentNode, boardLength, boardHeight)
        swappableTile = nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1] + 1]
        nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1] + 1] = nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1]]
        nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1]] = swappableTile
        listOfSuccessorNodes.append(nextNode)
        # print("▊ Next node: ", nextNode)
    # check if empty space can be swapped with left-adjacent tile, then swap
    if indexOfEmptySpace[1] > 0: 
        # print("▊ Swap left")
        nextNode = deepCopy(currentNode, boardLength, boardHeight)
        swappableTile = nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1] - 1]
        nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1] - 1] = nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1]]
        nextNode[indexOfEmptySpace[0]][indexOfEmptySpace[1]] = swappableTile
        listOfSuccessorNodes.append(nextNode)
        # print("▊ Next node: ", nextNode)

    return sorted(listOfSuccessorNodes)






def AStarIDSComparisonWithFile():
    # initialize board 
    goalState = [[0,1,2],[3,4,5],[6,7,8]]
    boardLength = 3
    boardHeight = 3
    initialNode = [[0 for _ in range(boardLength)] for _ in range(boardHeight)]

    # read file 
    puzzleDatabaseFile = ""
    with open('project-1-instructions/Length4-1.txt', 'r') as file:
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
        frontierQ = []
        heapq.heappush(frontierQ, (summedManhattanDistance(initialNode), initialNode))

        while len(frontierQ) > 0: 
            currentNode = frontierQ[0][1]
            if currentNode == goalState:
                return currentCost
            
            # Exploring each successor node
            successorNodes = findSuccessorNodes(currentNode, boardLength, boardHeight)
            while len(successorNodes) > 0: 
                successorNode = successorNodes.pop()
                successorCurrentCost = currentCost + 1  # The cost to get to the next state is always
                                                        # just +1 because tiles can only move 1 step at a time
                # check if this successor is already in the frontier 
                for node in range(len(frontierQ)): 
                    if (successorNode in frontierQ[node]):
                        print("▊", True)
                        if currentCost <= successorCurrentCost: continue
                        elif successorNode in exploredNodes:
                            if currentCost <= successorCurrentCost: continue
                            heapq.heappush(frontierQ, (successorCurrentCost, successorNode))
                        else: 
                            heapq.heappush(frontierQ, (successorCurrentCost, successorNode))
                            heuristicCost = summedManhattanDistance(successorNode)
                        currentCost = successorCurrentCost
                        # FIGURE OUT HOW TO SET THE PARENT TO THE CURRENT NODE 
                        # class Node:
                        #     def __init__(self, state):
                        #         self.state = state
                        #         self.parent = None
                        #         self.g = 0
                        #         self.h = 0

                        # # Set parent
                        # node_successor.parent = node_current
                # Add it to the explored list and remove from frontier
                exploredNodes.append(currentNode)
                heapq.heappop(frontierQ)

            if currentNode != goalState: return "Error"
            



            # while len(successorNodes) > 0: 
            #     heapq.heappush(frontierQ, (summedManhattanDistance(successorNodes[0]) + 1, successorNodes.pop()))
                
            while len(frontierQ) > 0:
                print("▊", heapq.heappop(frontierQ))
            
                # successorNode = successorNodes.pop()
                # successorCurrentCost = summedManhattanDistance(successorNode) + 1  # The cost to get to the next state is always
                #                                         # just 1 because tiles can only move 1 step at a time


if __name__ == "__main__":

    AStarIDSComparisonWithFile()
    # AStarIDSComparisonWithInput()