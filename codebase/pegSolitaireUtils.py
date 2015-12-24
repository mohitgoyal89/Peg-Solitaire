import readGame
import config


#######################################################
# These are some Helper functions which you have to use 
# and edit.
# Must try to find out usage of them, they can reduce
# your work by great deal.
#
# Functions to change:
# 1. is_wall(self, pos):
# 2. is_validMove(self, oldPos, direction):
# 3. getNextPosition(self, oldPos, direction):
# 4. getNextState(self, oldPos, direction):
#######################################################

class game:
    def __init__(self, filePath):
        self.gameState = readGame.readGameState(filePath)
        self.nodesExpanded = 0
        self.trace = []

    # function to check corner positions in game state
    def is_corner(self, pos):
        rIndex = pos[0]
        cIndex = pos[1]
        # check if the position is in 1st or last row or column
        if rIndex in [0, 6] or cIndex in [0, 6]:
            return True
        else:
            return False

    # util function to check unusuable position in board where no peg can be placed
    def isUnusuablePosition(self, pos):
        rIndex = pos[0]
        cIndex = pos[1]
        cornerIndices = [0, 1, 5, 6]
        if rIndex in cornerIndices:
            if cIndex in cornerIndices:
                return True
        else:
            return False

    # getNextPosition() will give the 2nd next postion from the given position
    def getNextPosition(self, oldPos, direction):
        #########################################
        # Get the new position from the given
        if config.DIRECTION.has_key(direction):
            dir = config.DIRECTION.get(direction)
            newPos = [(oldPos[0] + 2 * dir[0]), (oldPos[1] + 2 * dir[1])]
            return newPos

    # to check whether a move is valid or not in a given direction for a given position:oldPos
    def is_validMove(self, oldPos, direction):
        #########################################
        # DONT change Things in here
        # In this we have got the next peg position and
        # below lines check for if the new move is a corner
        newPos = self.getNextPosition(oldPos, direction)
        if self.isUnusuablePosition(newPos):
            return False

        # Check if neighbour is occupied in the given direction
        if not self.isNeighbourOccupied(oldPos, direction):
            # print "For direction : " +str(direction) + ", Neighbour is 0 for " + str(oldPos)
            return False

        rIndex = newPos[0]
        cIndex = newPos[1]
        # check for row index bounds
        if rIndex < 0 or rIndex >= len(self.gameState):
            # print "For direction : " +str(direction) + ", Invalid Row index" + str(rIndex)
            return False

        # check for column index bounds
        elif cIndex < 0 or cIndex >= len(self.gameState[0]):
            # print "For direction : " +str(direction) + ", Invalid Row index" + str(rIndex)
            return False

        # check whether the position already has a peg in it.
        elif self.gameState[rIndex][cIndex] == 1:
            # print "For direction : " +str(direction) + ", Invalid Row index" + str(rIndex)
            return False

        # Its a valid move, return True
        else:
            return True

    # This function checks whether the neighbour position in the given direction is valid and occupied
    def isNeighbourOccupied(self, oldPos, direction):
        dir = config.DIRECTION.get(direction)
        rIndex = oldPos[0] + dir[0]
        cIndex = oldPos[1] + dir[1]

        # check for out of index for row index
        if rIndex < 0 or rIndex >= len(self.gameState):
            return False

        # check for column index bounds
        elif cIndex < 0 or cIndex >= len(self.gameState[0]):
            return False

        # check for neighbour occupancy
        if self.gameState[rIndex][cIndex] == 1:
            return True
        else:
            return False

    # getNextState() gives the next game state if exists from a given position in the given direction
    def getNextState(self, oldPos, direction):
        ###############################################
        # DONT Change Things in here
        self.nodesExpanded += 1
        if not self.is_validMove(oldPos, direction):
            print "Error, You are not checking for valid move"
            exit(0)
        ###############################################

        newPos = self.getNextPosition(oldPos, direction)
        # set the new  position value to 1
        self.gameState[newPos[0]][newPos[1]] = 1
        # set the value of crossed over peg to 0
        if direction == 'N':
            self.gameState[oldPos[0] - 1][oldPos[1]] = 0
        elif direction == 'S':
            self.gameState[oldPos[0] + 1][oldPos[1]] = 0
        elif direction == 'E':
            self.gameState[oldPos[0]][oldPos[1] + 1] = 0
        elif direction == 'W':
            self.gameState[oldPos[0]][oldPos[1] - 1] = 0

        # set oldPos peg value to 0
        self.gameState[oldPos[0]][oldPos[1]] = 0
        self.trace.append(tuple(oldPos))
        self.trace.append(tuple(newPos))
        return self.gameState

    # check for goal state
    @staticmethod
    def isGoalState(currentState, goalState):
        if (currentState == goalState):
            return True
        return False


GOAL_STATE = [[-1, -1, 0, 0, 0, -1, -1],
              [-1, -1, 0, 0, 0, -1, -1],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [-1, -1, 0, 0, 0, -1, -1],
              [-1, -1, 0, 0, 0, -1, -1]]


# check for node already visited nodes for pruning
def isAlreadyVisited(visited, newGameState):
    for state in visited:
        if state == newGameState:
            return True
    return False


# Heuristic1: uses manhattan heurisitic to calculate the cost of
# moving pegs to goal state depending upon distance
def heuristic1(gameState):
    distFromGoal = 0
    for rIndex, rData in enumerate(gameState):
        for cIndex, cData in enumerate(rData):
            if (gameState[rIndex][cIndex] == 1):
                distFromGoal += abs(rIndex - 3) + abs(cIndex - 3)
    return distFromGoal


# Heuristic2: Uses minimum of number of isolated  pegs and manhattan distance for game state as heuristic to
# decide which game state to expand to reach to the goal state
# For each board position we check whether the peg has neighbours or not. So we count the number of isolated pegs
# on the board and add it to manhattan distance for each game state to give a better heuristic function.
def heuristic2(gameState):
    isolatedPegCount = 0
    mDis = heuristic1(gameState)
    for rIndex, rData in enumerate(gameState):
        for cIndex, cData in enumerate(rData):
            if (gameState[rIndex][cIndex] == 1):
                oldPos = [rIndex, cIndex]
                count = 0
                for direction in config.DIRECTION.keys():
                    dir = config.DIRECTION.get(direction)
                    newPos = [oldPos[0] + dir[0], oldPos[1] + dir[1]]
                    # check for valid position on board
                    cornerIndices = [0, 1, 5, 6]
                    if newPos[0] in cornerIndices:
                        if newPos[1] in cornerIndices:
                            count += 1
                    # check for index bounds
                    if newPos[0] < 0 or newPos[0] > 6 or newPos[1] < 0 or newPos[1] > 6:
                        count += 1
                        break

                    if gameState[newPos[0]][newPos[1]] == 0:
                        count += 1
                if count == 4:
                    # count 4 means there is no valid neighbour peg
                    isolatedPegCount += 1
    return isolatedPegCount + mDis








