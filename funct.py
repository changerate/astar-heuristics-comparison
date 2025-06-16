def manhattanDistance(state, goalState):
    i = 0
    # print("(", state % 3, int(state /3 ), ")")
    horizontalDistance = abs(state % 3 - goalState % 3)
    verticalDistance = abs(int(state / 3) - int(goalState / 3))
    distance = verticalDistance + horizontalDistance
    # print(verticalDistance)
    # print(horizontalDistance)
    print(distance)


for i in range(9):
    manhattanDistance(i, 0)