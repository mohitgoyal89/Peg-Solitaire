import heapq


# Stack class is used to provide LIFO operation in Iterative deepening DFS tree
class Stack:
    def __init__(self):
        self.stack = []

    def push(self, node):
        self.stack.append(node)

    def pop(self):
        if not self.isEmpty():
            return self.stack.pop()

    def isEmpty(self):
        return len(self.stack) == 0

    def peek(self):
        if not self.isEmpty():
            return self.stack[-1]


# StackNode encapsulates the game state and depth of a particular node in Iterative Deepening search
class IDSNode:
    def __init__(self, nodeData, depth):
        self.nodeData = nodeData
        self.depth = depth


# AStarNode encapsulates the game state and number of moves in A Star Search
class AStarNode:
    def __init__(self, nodeData, nMoves):
        self.nodeData = nodeData
        self.nMoves = nMoves


# HeapQueue is used to store heuristic cost and nodes and will return the nodes with minimum heuristic on pop
class HeapQueue:
    def __init__(self):
        self.heapQueue = []

    def isHeapEmpty(self):
        return len(self.heapQueue) == 0

    def heapPush(self, heurCost, heapQueueNode):
        heapq.heappush(self.heapQueue, (heurCost, heapQueueNode))

    def heapPop(self):
        return heapq.heappop(self.heapQueue)
