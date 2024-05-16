from random import random

# Constants
EMPTY = 0
RESOURCE = 1

class Board:

    # Class Constructor
    def __init__(self, board_size, resource_frequency=.1, resource_growth_frequency=.5, timestamp=0):
        self.setBoardSize(board_size)
        self.setResourceFrequency(resource_frequency)
        self.setResourceGrowthFrequency(resource_growth_frequency)        
        self.setTimestamp(timestamp)
        self.board = [[self.Cell() for i in range(board_size)] for j in range(board_size)]

    # Inner Class
    class Cell:
        # Inner Class Constructor
        def __init__(self, resource=EMPTY, agent=None, timestamp=0):
            self.setAgent(agent)
            self.setResource(resource)
            self.setTimestamp(timestamp)

        # Inner Class Getters/Setters

        def getResource(self):
            return self.resource
        
        def getAgent(self):
            return self.agent
        
        def setResource(self, resource):
            self.resource = resource

        def setAgent(self, agent):
            self.agent = agent

        def getTimestamp(self):
            return self.timestamp
        
        def setTimestamp(self, timestamp):
            self.timestamp = timestamp

        # Inner Class Methods

        def noResource(self):
            return self.getResource() == EMPTY
        
        def addResource(self):
            self.setResource(RESOURCE)

        def removeResource(self):
            self.setResource(EMPTY)

        def noAgent(self):
            return self.getAgent() is None

        def removeAgent(self):
            agent = self.getAgent()
            self.setAgent(None)
            return agent

        def isOlder(self, other):
            if not isinstance(other, self.__class__):
                raise TypeError("Cannot compare different types.")
            
            return self.getTimestamp() < other.getTimestamp()

        def __str__(self):
            output = "("
            if self.noResource():
                output += "Empty; "
            else:
                output += "Resource; "
            if self.noAgent():
                output += "No Agent; "
            else:
                output += "Agent; "
            output = str(self.getTimestamp()) + ")"
            return output
        
    def manhattanDistance(self, i1, j1, i2, j2):
        return abs(i1 - i2) + abs(j1 - j2)
        
    # Class Getters/Setters

    def getBoardSize(self):
        return self.board_size
    
    def getBoard(self):
        return self.board
    
    def getResourceFrequency(self):
        return self.resource_frequency

    def getResourceGrowthFrequency(self):
        return self.resource_growth_frequency
    
    def getCell(self, i, j):
        return self.board[i][j]
    
    def getTimestamp(self):
        return self.timestamp
    
    def setCell(self, i, j, cell):
        self.board[i][j] = cell

    def setTimestamp(self, timestamp):
        self.timestamp = timestamp

    # Class Methods

    def deepCopy(self):
        copy = Board(self.getBoardSize(), self.getResourceFrequency(),
                      self.getResourceGrowthFrequency(), self.getTimestamp())
        
        for i in range(self.getBoardSize()):
            for j in range(self.getBoardSize()):
                cell = self.getCell(i, j)
                copy.setCell(i, j, self.Cell(cell.getResource(), cell.getAgent(), cell.getTimestamp()))

        return copy

    def incrementTimestamp(self):
        self.setTimestamp(self.getTimestamp() + 1)

    def isCell(self, i, j):
        return i >= 0 and i < self.board_size and j >= 0 and j < self.board_size

    def noAgent(self, i, j):
        return self.getCell(i, j).noAgent()
    
    def addAgent(self, i, j, agent):
        self.getCell(i, j).setAgent(agent)

    def removeAgent(self, i, j):
        return self.getCell(i, j).removeAgent()

    def noResource(self, i, j):
        return self.getCell(i, j).noResource()

    def hasResource(self, i, j):
        return not self.noResource(i, j)

    def countNeighborResources(self, i, j):
        count = 0
        if self.isCell(i - 1, j) and self.hasResource(i - 1, j):
            count = count + 1
        if self.isCell(i + 1, j) and self.hasResource(i + 1, j):
            count = count + 1
        if self.isCell(i, j - 1) and self.hasResource(i, j - 1):
            count = count + 1
        if self.isCell(i, j + 1) and self.hasResource(i, j + 1):
            count = count + 1
        return count

    def addResource(self, i, j):
        self.getCell(i, j).addResource()

    def removeResource(self, i, j):
        self.getCell(i, j).removeResource()
    
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
        growth_positions = []
        for i in range(self.getBoardSize()):
            for j in range(self.getBoardSize()):
                if (self.noResource(i, j)):
                    if random() < self.getResourceGrowthFrequency() * self.countNeighborResources(i, j):
                        growth_positions.append((i, j))

        for (i, j) in growth_positions:
            self.addResource(i, j)

    def resetBoard(self):
        self.board = [[self.Cell() for i in range(self.getBoardSize())] for j in range(self.getBoardSize())]

    def printBoard(self):
        for i in range(self.getBoardSize()):
            for j in range(self.getBoardSize()):
                print(self.getCell(i, j), end=" ")
            print()
        print()

    def hasResource(self, i, j):
        return not self.noResource(i, j)
    
    def validPosition(self, i, j):
        return i >= 0 and i < self.getBoardSize() and j >= 0 and j < self.getBoardSize()
    
    def moveAgent(self, old_i, old_j, new_i, new_j):
        if not self.validPosition(old_i, old_j) or not self.validPosition(new_i, new_j):
            raise ValueError("Invalid position.")
        if self.noAgent(old_i, old_j):
            raise ValueError("No agent at the given position.")
        if not self.noAgent(new_i, new_j):
            raise ValueError("Another agent already at the new position.")
        
        agent = self.removeAgent(old_i, old_j)
        self.addAgent(new_i, new_j, agent)

    # Shortest path between two points (return a plan)
    def shortestPath(self, i1, j1, i2, j2):
        queue = [(i1, j1)]
        parent = {(i1, j1): None}
        path = []
        visited = []
        while queue:
            i, j = queue.pop(0)
            if i == i2 and j == j2:
                current = (i, j)
                while current:
                    path.insert(0, current)
                    current = parent[current]
                return path
            if (i, j) not in visited:
                visited.append((i, j))
                if self.validPosition(i - 1, j) and self.noAgent(i - 1, j):
                    queue.append((i - 1, j))
                    parent[(i - 1, j)] = (i, j)
                if self.validPosition(i + 1, j) and self.noAgent(i + 1, j):
                    queue.append((i + 1, j))
                    parent[(i + 1, j)] = (i, j)
                if self.validPosition(i, j - 1) and self.noAgent(i, j - 1):
                    queue.append((i, j - 1))
                    parent[(i, j - 1)] = (i, j)
                if self.validPosition(i, j + 1) and self.noAgent(i, j + 1):
                    queue.append((i, j + 1))
                    parent[(i, j + 1)] = (i, j)
        return []


    # Compute the shortest path from (i1, j1) to another cell, 
    # with an apple using a, breadth-first search algorithm.
    # If a cell contains an agent, it is considered an obstacle. 
    # The algorithm should also build a list of the cells that form the path.
    def shortestPath(self, i1, j1):
        # Initialize the queue with the starting cell
        queue = [(i1, j1)]
        # Initialize the dictionary that will store the parent of each cell
        parent = {(i1, j1): None}
        # Initialize the list that will store the path
        path = []
        # Initialize the list that will store the cells that have been visited
        visited = []
        # While the queue is not empty
        while queue:
            # Dequeue the first cell in the queue
            i, j = queue.pop(0)
            # If the cell contains an apple
            if self.hasResource(i, j):
                # Initialize the current cell
                current = (i, j)
                # While the current cell is not the starting cell
                while current:
                    # Add the current cell to the path to start of the path
                    path.insert(0, current)
                    # Update the current cell to the parent of the current cell
                    current = parent[current]
                # Return the path
                return path
            # If the cell has not been visited
            if (i, j) not in visited:
                # Mark the cell as visited
                visited.append((i, j))
                # If the cell to the left is valid
                if self.validPosition(i - 1, j):
                    # If the cell to the left is not an obstacle
                    if self.noAgent(i - 1, j):
                        # Enqueue the cell to the left
                        queue.append((i - 1, j))
                        # Set the parent of the cell to the left to the current cell
                        parent[(i - 1, j)] = (i, j)
                # If the cell to the right is valid
                if self.validPosition(i + 1, j):
                    # If the cell to the right is not an obstacle
                    if self.noAgent(i + 1, j):
                        # Enqueue the cell to the right
                        queue.append((i + 1, j))
                        # Set the parent of the cell to the right to the current cell
                        parent[(i + 1, j)] = (i, j)
                # If the cell above is valid
                if self.validPosition(i, j - 1):
                    # If the cell above is not an obstacle
                    if self.noAgent(i, j - 1):
                        # Enqueue the cell above
                        queue.append((i, j - 1))
                        # Set the parent of the cell above to the current cell
                        parent[(i, j - 1)] = (i, j)
                # If the cell below is valid
                if self.validPosition(i, j + 1):
                    # If the cell below is not an obstacle
                    if self.noAgent(i, j + 1):
                        # Enqueue the cell below
                        queue.append((i, j + 1))
                        # Set the parent of the cell below to the current cell
                        parent[(i, j + 1)] = (i, j)
        # If no path is found, return an empty list
        return []

    def __str__(self):
        return "Board Size: " + str(self.getBoardSize()) + "\n" + \
               "Resource Frequency: " + str(self.getResourceFrequency()) + "\n" + \
               "Board: " + self.printBoard()
    
