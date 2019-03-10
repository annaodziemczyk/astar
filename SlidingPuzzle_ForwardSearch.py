import random
from enum import Enum
import math
from copy import deepcopy

class AStarSearch:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.openNodes = []
        self.closedNodes = []

    def solve(self):
        print("Looking for solution....")
        self.openNodes.append(self.puzzle)
        #print("COST " + str(self.puzzle.cost))
        while len(self.openNodes) > 0:
            #print("open nodes:{0} closed nodes:{1}".format(len(self.openNodes), len(self.closedNodes)))
            self.openNodes.sort(key=lambda n: n.cost)
            current = self.openNodes[0]
            #current.displayPuzzleState(current.state, str(current.cameFromDirection))
            if current.cost == 0:
                self.showSolution(current)
                break

            del self.openNodes[0]
            self.closedNodes.append(current)

            neighbours = self.findChildStates(current)

            for direction, state in neighbours.items():
                state.cameFromDirection = direction
                if state in self.closedNodes:
                    continue
                if state not in self.openNodes:
                    self.openNodes.append(state)
                else:
                    continue

                if state.cost >= current.cost:
                    continue

    def showSolution(self, leafnode):
        path = []
        while leafnode.parent:
            path.append(leafnode)
            leafnode = leafnode.parent
        path.reverse()
        print("SOLUTION (moves - {0})".format(len(path)))
        for state in path:
            leafnode.displayPuzzleState(state.state, str(state.cameFromDirection))

    def findChildStates(self, state):
        neighbours={}
        possiblemoves = state.getPossibleMoves()
        for move in possiblemoves:
            neighbour = Puzzle(state.width, state.height)
            neighbour.clone(state)
            neighbour.move(move)
            neighbour.parent = state
            #print("{0} cost {1}".format(move, neighbour.cost))
            neighbours[move] = neighbour
        return neighbours

class Move(Enum):
    UP = "move up"
    DOWN = "move down"
    LEFT = "move left"
    RIGHT = "move right"

class Puzzle:
    MOVING_BLOCK_VALUE = 0
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.state = []
        self.cost = 0
        self.parent = None
        self.currentPosition = 0

    def clone(self, state):
        self.state = deepcopy(state.state)
        self.cost = state.cost
        self.currentPosition = state.currentPosition

    def initialize(self):
        self.state = self.getGoalState()
        random.shuffle(self.state)
        #self.state = [1,2,3,4,5,6,0,7,8]
        while not self.isSolvable(self.state):
            random.shuffle(self.state)

        for index in range(len(self.state)):
            if self.state[index] == self.MOVING_BLOCK_VALUE:
                self.currentPosition = index
            else:
                nodeCost = self.calculateManhattanDistance(self.state[index], index)
                #print("node {0} cost {1}".format(self.state[index], nodeCost))
                self.cost = self.cost + nodeCost

        #print("COST " + str(self.cost))
        self.displayPuzzleState(self.state, "Initial")

    def isSolvable(self, initialstate):
        inversCount = 0

        for i in range(len(initialstate)):
            if initialstate[i] == self.MOVING_BLOCK_VALUE:
                continue
            for j in range(i, len(initialstate)):
                if initialstate[j] == self.MOVING_BLOCK_VALUE:
                    continue
                if initialstate[i] > initialstate[j]:
                    inversCount += 1

        if self.width % 2 != 0 or math.floor(initialstate.index(self.MOVING_BLOCK_VALUE)/self.width) % 2 == 0:
            return inversCount % 2 == 0

        return inversCount % 2 != 0

    def getGoalState(self):
        goalstate = list(range(1, self.width * self.height))
        goalstate.append(self.MOVING_BLOCK_VALUE)
        self.displayPuzzleState(goalstate, "Goal")
        return goalstate.copy()

    def displayPuzzleState(self, state, name):
        print("*** %s State***" % name)
        print("|-----------|", end=" ")
        for i in range(len(state)):
            if i % self.width == 0:
                print("\n|", end=" ")
            print("%s |" % state[i], end=" ")
        print("\n|-----------|")

    def calculateManhattanDistance(self, value, index):
        goalindex = value - 1
        if goalindex < index:
            if index - goalindex < self.width:
                return index - goalindex
            else:
                rowdifference = math.floor((index - goalindex)/3)
                return rowdifference + (index - rowdifference * self.width) - goalindex
        elif goalindex > index:
            if goalindex - index < self.width:
                return goalindex - index
            else:
                rowdifference = math.floor((goalindex - index)/3)
                return rowdifference + goalindex - (index + rowdifference * self.width)
        return 0

    def move(self, action):
        movetoindex = self.findFieldIndex(action)

        if movetoindex >= 0 and movetoindex < len(self.state):
            swapValue = self.state[movetoindex]
            self.cost = self.cost - self.calculateManhattanDistance(swapValue, movetoindex)
            self.state[self.currentPosition] = deepcopy(swapValue)
            self.calculateManhattanDistance(self.state[self.currentPosition], self.currentPosition)
            self.cost = self.cost + self.calculateManhattanDistance(self.state[self.currentPosition], self.currentPosition)
            self.state[movetoindex] = self.MOVING_BLOCK_VALUE

            self.currentPosition = movetoindex

            #print(action)
            #self.displayPuzzleState(self.state, "Current")
        else:
            print("Can't %s" % action)

    def findFieldIndex(self, action):
        moveToIndex = -1
        if action == Move.UP and self.currentPosition-self.width >= 0:
            moveToIndex = self.currentPosition-self.width
        elif action == Move.DOWN and self.currentPosition + self.width < len(self.state):
            moveToIndex = self.currentPosition + self.width
        elif action == Move.RIGHT and (self.currentPosition + 1) % self.width != 0:
            moveToIndex = self.currentPosition + 1
        elif action == Move.LEFT and self.currentPosition % self.width != 0:
            moveToIndex = self.currentPosition - 1

        return moveToIndex

    def getPossibleMoves(self):
        moves = []
        for direction in Move:
            index = self.findFieldIndex(direction)
            if index != -1:
                moves.append(direction)
        return moves

    def __str__(self):
        return str(self.displayPuzzleState(self.state, ""))

    def __repr__(self):
        return str(self.displayPuzzleState(self.state, ""))

if __name__ == "__main__":
    puzzle = Puzzle(3,3)
    puzzle.initialize()
    aStar = AStarSearch(puzzle)
    aStar.solve()