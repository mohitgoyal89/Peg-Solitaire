import copy
import time
from sys import maxint
import config
import pegSolitaireUtils
import pegSolitaireCollections

LIMIT_REACHED = 0
GOAL_FOUND = 1
INVALID_STATE = 2

# ItrDeepSearch function uses Depth limited search in an iterative manner to find out goal state
# A stack is used to explore nodes in a depth first search manner upto the limited depth in each step
# EXTRA_CREDIT
# A visited nodes list is maintained to prune game states that have been
# already explored earlier that doesn't reach to goal state
def ItrDeepSearch(pegSolitaireObject):
    stack = pegSolitaireCollections.Stack()
    for depth in xrange(0, maxint):
        visited = []
        val = depthLimitedSearch(stack, pegSolitaireObject, depth, visited)
        if  val == GOAL_FOUND:
            return True
        elif val == INVALID_STATE:
            return False

# Depth limited search is applied for incremental depth value and game states are expanded till a goal state is found
# or the stack is empty before the depth linit is reached in which case the given input is invalid
def depthLimitedSearch(stack, startGameObj, depth, visited):
    exp = 0
    idsNode = pegSolitaireCollections.IDSNode(startGameObj, 0)
    stack.push(idsNode)
    while not stack.isEmpty():
        topNode = stack.pop()
        if (pegSolitaireUtils.game.isGoalState(topNode.nodeData.gameState, pegSolitaireUtils.GOAL_STATE)):
            startGameObj.nodesExpanded = exp
            startGameObj.trace = topNode.nodeData.trace
            return GOAL_FOUND
        exp += 1
        visited.append(topNode.nodeData.gameState)
        currDepth = topNode.depth
        if  currDepth + 1 <= depth:
            for rIndex, rowData in enumerate(topNode.nodeData.gameState):
                for cIndex, columnData in enumerate(rowData):
                    oldPos = [rIndex, cIndex]
                    expandPosition(topNode, oldPos, stack, visited, 'IDS')
        else:
            return LIMIT_REACHED
    if  stack.isEmpty():
        print "Iterative Deepening search solution does not exist for this board state"
        return INVALID_STATE

# expandPosition function call getNextState and push new game objects to stack or heapQueue
# depending upon the search algorithm
def expandPosition(node, oldPos, dataStructure, visited, searchAlgo):
    if (not node.nodeData.isUnusuablePosition(oldPos)) and node.nodeData.gameState[oldPos[0]][oldPos[1]] == 1:
        for dir in config.DIRECTION.keys():
            if node.nodeData.is_validMove(oldPos, dir):
                newGameObj = copy.deepcopy(node.nodeData)
                newGameState = newGameObj.getNextState(oldPos, dir)
                if not pegSolitaireUtils.isAlreadyVisited(visited, newGameState):
                    if searchAlgo == 'IDS':
                        # print 'IDS'
                        dataStructure.push(pegSolitaireCollections.IDSNode(newGameObj, node.depth + 1))
                    elif searchAlgo == 'aOne':
                        # print 'aOne'
                        heurCost = pegSolitaireUtils.heuristic1(newGameObj.gameState) + node.nMoves
                        dataStructure.heapPush(heurCost, pegSolitaireCollections.AStarNode(newGameObj, node.nMoves + 1))
                    elif searchAlgo == 'aTwo':
                        # print 'aTwo'
                        heurCost = pegSolitaireUtils.heuristic2(newGameObj.gameState) + node.nMoves
                        dataStructure.heapPush(heurCost, pegSolitaireCollections.AStarNode(newGameObj, node.nMoves + 1))

# aStar function  in an iterative manner to find out goal state
# A heapQueue is used to store nodes, nMoves and heurCost
# EXTRA_CREDIT
# A visited nodes list is maintained to prune game states that have been
# already explored earlier that doesn't reach to goal state
def aStar(aStarObject, heuristic):
    exp = 0
    visited = []
    heapQueue = pegSolitaireCollections.HeapQueue()
    aStarNode = pegSolitaireCollections.AStarNode(aStarObject, 0)
    heapQueue.heapPush(0, aStarNode)
    while not heapQueue.isHeapEmpty():
        frontQueue = heapQueue.heapPop()
        frontNode = frontQueue[1]
        if (pegSolitaireUtils.game.isGoalState(frontNode.nodeData.gameState, pegSolitaireUtils.GOAL_STATE)):
            aStarObject.nodesExpanded = exp
            aStarObject.trace = frontNode.nodeData.trace
            return True
        exp += 1
        visited.append(frontNode.nodeData.gameState)
        for rIndex, rData in enumerate(frontNode.nodeData.gameState):
            for cIndex, cData in enumerate(rData):
                oldPos = [rIndex, cIndex]
                expandPosition(frontNode, oldPos, heapQueue, visited, heuristic)
    return False


# aStarOne function uses heuristic1 function to minimize the number of heuristic cost to reach the goal state
def aStarOne(pegSolitaireObject):
    aOneStartGameObj = pegSolitaireObject
    if (aStar(aOneStartGameObj, 'aOne')):  # passing aOneStartGameObj to aStar to find the solution
        return True
    print "A* one solution does not exist for this board state"
    return False


# aStarOne function uses heuristic2 function to minimize the number of heuristic cost to reach the goal state
def aStarTwo(pegSolitaireObject):
    aTwoStartGameObj = pegSolitaireObject
    if (aStar(aTwoStartGameObj, 'aTwo')):  # passing aTwoStartGameObj to aStar to find the solution
        return True
    print "A* two solution does not exist for this board state"
    return False