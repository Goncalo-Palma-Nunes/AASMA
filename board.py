from random import random

EMPTY = 0
RESOURCE = 1
AGENT = 2
NO_AGENT = 3

class Board:
    def __init__(self, board_size, resource_frequency=.1, resource_growth_frequency=.5):
        self.setBoardSize(board_size)
        self.setResourceFrequency(resource_frequency)
        self.setResourceGrowthFrequency(resource_growth_frequency)
        self.board = [[[EMPTY, NO_AGENT] for i in range(board_size)] for j in range(board_size)]

    def __convertCellToString(self, cell):
        output = "("
        for i in cell:
            if i == EMPTY:
                output += "Empty; "
            elif i == RESOURCE:
                output += "Resource; "
            elif i == AGENT:
                output += "Agent; "
            elif i == NO_AGENT:
                output += "No Agent; "
        output = output[:-2] + ")"
        return output

    def getBoardSize(self):
        return self.board_size
    
    def getBoard(self):
        return self.board
    
    def getResourceFrequency(self):
        return self.resource_frequency
    
    def getCell(self, i, j):
        return self.board[i][j]
    
    def setCell(self, i, j, cell):
        self.board[i][j] = cell

    def isCell(self, i, j):
        return i >= 0 and i < self.board_size and j >= 0 and j < self.board_size

    def noAgent(self, i, j):
        return self.getCell(i, j)[1] == NO_AGENT
    
    def addAgent(self, i, j):
        self.setCell(i, j, (self.getCell(i, j)[0], AGENT))

    def removeAgent(self, i, j):
        self.setCell(i, j, (self.getCell(i, j)[0], NO_AGENT))

    def noResource(self, i, j):
        return self.getCell(i, j)[0] == EMPTY

    def hasResource(self, i, j):
        return self.isCell(i, j) and self.getCell(j, j)[0] == RESOURCE

    def countNeighborResources(self, i, j):
        count = 0
        if self.hasResource(i - 1, j):
            count = count + 1
        if self.hasResource(i + 1, j):
            count = count + 1
        if self.hasResource(i, j - 1):
            count = count + 1
        if self.hasResource(i, j + 1):
            count = count + 1
        return count

    def addResource(self, i, j):
        self.setCell(i, j, (RESOURCE, self.getCell(i, j)[1]))

    def removeResource(self, i, j):
        self.setCell(i, j, (EMPTY, self.getCell(i, j)[1]))
    
    def setBoardSize(self, board_size):
        if not isinstance(board_size, int):
            raise TypeError("Board size must be an integer.")
        self.board_size = board_size

    def setResourceFrequency(self, resource_frequency):
        if (not isinstance(resource_frequency, float) or resource_frequency < 0 
            or resource_frequency > 1):
            raise TypeError("Resource frequency must be a valid probability value.")
        self.resource_frequency = resource_frequency

    def setResourceGrowthFrequency(self, resource_growth_frequency):
        if (not isinstance(resource_growth_frequency, float) or resource_growth_frequency < 0 
            or resource_growth_frequency > 1):
            raise TypeError("Resource growth frequency must be a valid probability value.")
        self.resource_growth_frequency = resource_growth_frequency

    def generateResources(self):
        for i in range(self.getBoardSize()):
            for j in range(self.getBoardSize()):
                if (self.noResource(i, j)
                    and random() < self.getResourceFrequency()):
                    self.addResource(i, j)

    def growResources(self):
        for i in range(self.getBoardSize()):
            for j in range(self.getBoardSize()):
                if (self.noResource(i, j))
                    if random() < self.getResourceGrowthFrequency() * self.countNeighborResources(i, j)
                        self.addResource(i, j)

    def resetBoard(self):
        self.board = [[(EMPTY, NO_AGENT) for i in range(self.getBoardSize())] for j in range(self.getBoardSize())]

    def printBoard(self):
        for i in range(self.getBoardSize()):
            for j in range(self.getBoardSize()):
                print(self.__convertCellToString(self.getCell(i, j)), end=" ")
            print()
        print()

    def hasResource(self, i, j):
        return self.getCell(i, j)[0] == RESOURCE
    
    def validPosition(self, i, j):
        return i >= 0 and i < self.getBoardSize() and j >= 0 and j < self.getBoardSize()
    
    def moveAgent(self, old_i, old_j, new_i, new_j):
        if not self.validPosition(old_i, old_j) or not self.validPosition(new_i, new_j):
            raise ValueError("Invalid position.")
        if self.noAgent(old_i, old_j):
            raise ValueError("No agent at the given position.")
        if not self.noAgent(new_i, new_j):
            raise ValueError("Another agent already at the new position.")
        
        self.removeAgent(old_i, old_j)
        self.addAgent(new_i, new_j)

    def __str__(self):
        return "Board Size: " + str(self.getBoardSize()) + "\n" + \
               "Resource Frequency: " + str(self.getResourceFrequency()) + "\n" + \
               "Board: " + self.printBoard()
    
