import random

class Board:
    ###########################
    ###     Constructor     ###
    ###########################

    def __init__(self, size):
        self.size = size
        self.cells = [[self.Cell() for i in range(size)] for j in range(size)]

    ###########################
    ###     Inner Class     ###
    ###########################

    class Cell:
        ###########################
        ###     Constructor     ###
        ###########################

        def __init__(self):
            self.resource = False
            self.agent = None
            self.timestamp = 0

        ###########################
        ### Getters and Setters ###
        ###########################

        def hasResource(self):
            return self.resource

        def setResource(self, resource):
            self.resource = resource

        def getAgent(self):
            return self.agent

        def setAgent(self, agent):
            self.agent = agent

        def getTimestamp(self):
            return self.timestamp

        def setTimestamp(self, timestamp):
            self.timestamp = timestamp

        ###########################
        ###       Methods       ###
        ###########################

        def putResource(self):
            self.setResource(True)

        def takeResource(self):
            resource = self.hasResource()
            self.setResource(False)
            return resource
        
        def hasAgent(self):
            return self.getAgent() is not None
            
        def putAgent(self, agent):
            if self.hasAgent():
                raise ValueError("Cell already has an agent.")
            self.setAgent(agent)

        def takeAgent(self):
            agent = self.getAgent()
            self.setAgent(None)
            return agent

        def merge(self, other):
            if not isinstance(other, self.__class__):
                raise TypeError("Cannot merge different types.")
            
            if other.getTimestamp() > self.getTimestamp():
                self.setResource(other.hasResource())
                self.setAgent(other.getAgent())
                self.setTimestamp(other.getTimestamp())

        ###########################
        ###       Overrides     ###
        ###########################

        def __str__(self):
            output = "("
            if self.hasResource():
                output += "Resource; "
            else:
                output += "Empty; "
            if self.hasAgent():
                output += "Agent; "
            else:
                output += "No Agent; "
            output += str(self.getTimestamp()) + ")"
            return output

    ###########################
    ### Getters and setters ###
    ###########################

    def getSize(self):
        return self.size
    
    def getCells(self):
        return self.cells
    
    def getCell(self, i, j):
        if not self.withinBounds(i, j):
            raise ValueError("Invalid cell position.")

        return self.cells[i][j]

    def getResourceCount(self):
        count = 0
        for line in self.getCells():
            for cell in line:
                if cell.hasResource():
                    count += 1
        return count

    ###########################
    ###       Methods       ###
    ###########################

    def estimateResourceCount(self, frequency):
        count = 0
        for i in range(self.getSize()):
            for j in range(self.getSize()):
                if self.hasResource(i, j):
                    count += 1
                elif self.getTimestamp(i, j) == 0:
                    count += frequency
        return count

    def manhattanDistance(self, i1, j1, i2, j2):
        return abs(i1 - i2) + abs(j1 - j2)

    def setTimestamp(self, timestamp):
        for line in self.getCells():
            for cell in line:
                cell.setTimestamp(timestamp)

    def withinBounds(self, i, j):
        return i >= 0 and i < self.size and j >= 0 and j < self.size

    def hasResource(self, i, j):
        return self.getCell(i, j).hasResource()

    def putResource(self, i, j):
        self.getCell(i, j).putResource()

    def takeResource(self, i, j):
        return self.getCell(i, j).takeResource()

    def hasAgent(self, i, j):
        return self.getCell(i, j).hasAgent()

    def isFreeToMove(self, i, j):
        return self.withinBounds(i, j) and not self.hasAgent(i, j)
    
    def putAgent(self, i, j, agent):
        self.getCell(i, j).putAgent(agent)

    def takeAgent(self, i, j):
        return self.getCell(i, j).takeAgent()

    def getTimestamp(self, i, j):
        return self.getCell(i, j).getTimestamp()
    
    def isSurroundedByResources(self, i, j):
        if self.withinBounds(i - 1, j) and not self.hasResource(i - 1, j):
            return False
        if self.withinBounds(i + 1, j) and not self.hasResource(i + 1, j):
            return False
        if self.withinBounds(i, j - 1) and not self.hasResource(i, j - 1):
            return False
        if self.withinBounds(i, j + 1) and not self.hasResource(i, j + 1):
            return False
        return True

    def hasSurroundedResource(self, i, j):
        return self.hasResource(i, j) and self.isSurroundedByResources(i, j)

    def countNeighborResources(self, i, j):
        count = 0
        if self.withinBounds(i - 1, j) and self.hasResource(i - 1, j):
            count = count + 1
        if self.withinBounds(i + 1, j) and self.hasResource(i + 1, j):
            count = count + 1
        if self.withinBounds(i, j - 1) and self.hasResource(i, j - 1):
            count = count + 1
        if self.withinBounds(i, j + 1) and self.hasResource(i, j + 1):
            count = count + 1
        return count

    def generateResources(self, resource_frequency):
        for i in range(self.size):
            for j in range(self.size):
                if random.random() < resource_frequency:
                    self.putResource(i, j)

    def growResources(self, growth_frequency):
        growth_positions = []
        for i in range(self.getSize()):
            for j in range(self.getSize()):
                if not self.hasResource(i, j):
                    if random.random() < growth_frequency * self.countNeighborResources(i, j):
                        growth_positions.append((i, j))

        for (i, j) in growth_positions:
            self.putResource(i, j)
            
    def getNumberOfResources(self):
        numberOfResources = 0
        for i in range(self.getSize()):
            for j in range(self.getSize()):
                if self.hasResource(i, j):
                    numberOfResources += 1
        return numberOfResources

    def moveAgent(self, old_i, old_j, new_i, new_j):
        if not self.withinBounds(old_i, old_j) or not self.withinBounds(new_i, new_j):
            raise ValueError("Invalid position.")
        if not self.hasAgent(old_i, old_j):
            raise ValueError("No agent at the given position.")
        if self.hasAgent(new_i, new_j):
            raise ValueError("Another agent already at the new position.")
        
        agent = self.takeAgent(old_i, old_j)
        self.putAgent(new_i, new_j, agent)

    def merge(self, other, rect=None):
        if not isinstance(other, self.__class__):
            raise TypeError("Cannot merge different types.")
        
        if other.getSize() != self.getSize():
            raise ValueError("Cannot merge boards of different sizes.")

        # Validate the merge rectangle
        if rect is None:
            rect = (0, 0, self.getSize() - 1, self.getSize() - 1)
        if not isinstance(rect, (list, tuple)) or len(rect) != 4:
            raise ValueError("Invalid rectangle.")
        min_i, min_j, max_i, max_j = rect

        # Update the states of the cells
        for i in range(min_i, max_i + 1):
            for j in range(min_j, max_j + 1):
                if self.withinBounds(i, j):
                    self.getCell(i, j).merge(other.getCell(i, j))

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
                if self.withinBounds(i - 1, j) and not self.hasAgent(i - 1, j):
                    queue.append((i - 1, j))
                    parent[(i - 1, j)] = (i, j)
                if self.withinBounds(i + 1, j) and not self.hasAgent(i + 1, j):
                    queue.append((i + 1, j))
                    parent[(i + 1, j)] = (i, j)
                if self.withinBounds(i, j - 1) and not self.hasAgent(i, j - 1):
                    queue.append((i, j - 1))
                    parent[(i, j - 1)] = (i, j)
                if self.withinBounds(i, j + 1) and not self.hasAgent(i, j + 1):
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
                if self.withinBounds(i - 1, j):
                    # If the cell to the left is not an obstacle
                    if not self.hasAgent(i - 1, j):
                        # Enqueue the cell to the left
                        queue.append((i - 1, j))
                        # Set the parent of the cell to the left to the current cell
                        parent[(i - 1, j)] = (i, j)
                # If the cell to the right is valid
                if self.withinBounds(i + 1, j):
                    # If the cell to the right is not an obstacle
                    if not self.hasAgent(i + 1, j):
                        # Enqueue the cell to the right
                        queue.append((i + 1, j))
                        # Set the parent of the cell to the right to the current cell
                        parent[(i + 1, j)] = (i, j)
                # If the cell above is valid
                if self.withinBounds(i, j - 1):
                    # If the cell above is not an obstacle
                    if not self.hasAgent(i, j - 1):
                        # Enqueue the cell above
                        queue.append((i, j - 1))
                        # Set the parent of the cell above to the current cell
                        parent[(i, j - 1)] = (i, j)
                # If the cell below is valid
                if self.withinBounds(i, j + 1):
                    # If the cell below is not an obstacle
                    if not self.hasAgent(i, j + 1):
                        # Enqueue the cell below
                        queue.append((i, j + 1))
                        # Set the parent of the cell below to the current cell
                        parent[(i, j + 1)] = (i, j)
        # If no path is found, return an empty list
        return []

    def getClosestResource(self, position, filter_fun=None, radius=None):
        """Return the closest position with a resource to the given position."""

        if radius is None:
            radius = self.getSize()
        min_distance = float('inf')

        for i in range(self.getSize()):
            for j in range(self.getSize()):
                if self.hasResource(i, j):
                    distance = self.manhattanDistance(position[0], position[1], i, j)
                    if distance < min_distance:
                        if filter_fun is None or filter_fun(i, j):
                            min_distance = distance
                            closest_position = (i, j)

        if min_distance <= radius:
            return closest_position
        else:
            return None

    def getNeighbors(self, i, j):
        neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        return [(i, j) for i, j in neighbors if self.withinBounds(i, j)]

    def anyAgentsInRadius(self, position, radius, ignore=None):
        i, j = position
        for k in range(i - radius, i + radius + 1):
            for l in range(j - radius, j + radius + 1):
                if self.withinBounds(k, l) and self.hasAgent(k, l) and (k, l) != ignore:
                        return True
        return False

    def getOldestPosition(self, filter_fun=None):
        oldest = None
        min_timestamp = float('inf')
        for i in range(self.getSize()):
            for j in range(self.getSize()):
                if self.getTimestamp(i, j) < min_timestamp:
                    if filter_fun is None or filter_fun(i, j):
                        oldest = (i, j)
                        min_timestamp = self.getTimestamp(i, j)
        return oldest

    def __str__(self):
        output = "Size: " + str(self.getSize()) + "\n" + \
                 "Cells:"
    
        for i in range(self.getSize()):
            for j in range(self.getSize()):
                output += str(self.getCell(i, j)) + " "
            output += "\n"
        return output
    
