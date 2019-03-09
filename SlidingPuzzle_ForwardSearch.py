import random
from enum import Enum

class Node:
    def __init__(self, index, value, gridWidth, gridHeight):
        self.index = index
        self.value = value
        self.y = index % gridWidth
        self.x = int(index / 3)

    def __str__(self):
        return "n<{0},{1}>={2}".format(self.x, self.y, self.value)

    def __repr__(self):
        return "n<{0},{1}>={2}".format(self.x, self.y, self.value)

class AStarSearch:
    def __init__(self, puzzle):
        self.puzzle = puzzle
    def solve(self):
        self.puzzle.displayProblem()

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
        self.goalState = list(range(1, width*height))
        self.goalState.append(self.MOVING_BLOCK_VALUE)
        self.initialState = self.goalState.copy()
        random.shuffle(self.initialState)
        self.currentState = self.initialState.copy()
        self.currentPosition = self.initialState.index(self.MOVING_BLOCK_VALUE)

    def move(self, action):

        moveToIndex = self.findFieldIndex(action)

        if moveToIndex >= 0 and moveToIndex < len(self.currentState):
            swapValue = self.currentState[moveToIndex]
            self.currentState[self.currentPosition] = swapValue
            self.currentState[moveToIndex] = self.MOVING_BLOCK_VALUE
            self.currentPosition = moveToIndex
            self.displayPuzzle(self.currentState, "Current")
        else:
            print("Can't %s" % action)

    def findFieldIndex(self, action):
        moveToIndex = -1
        if action == Move.UP and self.currentPosition-self.width >= 0:
            moveToIndex = self.currentPosition-self.width
        elif action == Move.DOWN and self.currentPosition + self.width < len(self.currentState):
            moveToIndex = self.currentPosition + self.width
        elif action == Move.RIGHT and (self.currentPosition + 1) % self.width != 0:
            moveToIndex = self.currentPosition + 1
        elif action == Move.LEFT and self.currentPosition % self.width != 0:
            moveToIndex = self.currentPosition - 1

        return moveToIndex

    def findNeighbours(self):
        neighbours = []
        for direction in Move:
            index = self.findFieldIndex(direction)
            if index != -1:
                neighbours.append(Node(index, self.currentState[index], self.width, self.height))
        return neighbours

    def displayProblem(self):
        self.displayPuzzleState(self.goalState, "Goal")
        self.displayPuzzleState(self.initialState, "Initial")
        print(self.findNeighbours())

    def displayPuzzleState(self, state, name):
        print("*** %s State***" % name)
        print("|-----------|", end =" ")
        for i in range(len(state)):
            if i % self.width == 0:
                print("\n|", end=" ")
            print("%s |" % state[i], end =" ")
        print("\n|-----------|")

if __name__ == "__main__":
    puzzle = Puzzle(3,3)
    aStar = AStarSearch(puzzle)
    aStar.solve()