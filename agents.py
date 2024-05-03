import abc
from board import Board
import itertools

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

class Agent:
    __metaclass__ = abc.ABCMeta
    id = itertools.count()
    
    def __init__(self, env : Board, endowment, utility_function, position=None, other_players=[]):
        self.setEnv(env)
        self.setEndowment(endowment)
        self.setUtilityFunction(utility_function)
        self.id = next(self.id)
        self.setOtherPlayers(other_players)
        self.position = position

    # Getters and setters

    def getEnv(self):
        return self.env
    
    def getEndowment(self):
        return self.endowment
    
    def getPosition(self):
        return self.position
    
    def getOtherPlayers(self):
        return self.other_players
    
    def utilityFunction(self):
        return self.utility_function
    
    def setEnv(self, env):
        if not isinstance(env, Board):
            raise ValueError("Environment must be of type Board.")
        self.env = env

    def setEndowment(self, endowment):
        self.endowment = endowment

    def setUtilityFunction(self, utility_function):
        if not callable(utility_function):
            raise ValueError("Utility function must be a callable function.")
        
        self.utility_function = utility_function

    def setPosition(self, position):
        if not isinstance(position, tuple) or len(position) != 2:
            raise ValueError("Position must be a tuple of length 2.")
        if any (i > self.getEnv().getBoardSize() for i in position):
            raise ValueError("Position must be within the bounds of the board.")
        self.position = position

    def setOtherPlayers(self, other_players):
        if not isinstance(other_players, (list, tuple)):
            raise ValueError("Other players must be a list or tuple.")
        if not all(isinstance(player, Agent) for player in other_players):
            raise ValueError("Other players must be a list or tuple of agents.")
        self.other_players = other_players

    # Methods

    def onResource(self):
        return self.getEnv().hasResource(self.getPosition()[0], self.getPosition()[1])
    
    def __validateMove(self, direction):
        new_position = self.getPosition()
        if direction == UP:
            new_position = (self.getPosition()[0] + 1, self.getPosition()[1])
        elif direction == DOWN:
            new_position = (self.getPosition()[0] - 1, self.getPosition()[1])
        elif direction == LEFT:
            new_position = (self.getPosition()[0], self.getPosition()[1] - 1)
        elif direction == RIGHT:
            new_position = (self.getPosition()[0], self.getPosition()[1] + 1)
        else:
            raise ValueError("Invalid direction. Must be 'up', 'down', 'left', or 'right'.")
        
        if not self.getEnv().validPosition(new_position[0], new_position[1]):
            raise ValueError("Cannot move out of bounds.")
        if not self.getEnv().noAgent(new_position[0], new_position[1]):
            raise ValueError("Cannot move to a position with another agent.")
        
        return new_position
    
    def move(self, direction):
        new_position = self.__validateMove(direction)
        
        self.getEnv().moveAgent(self.getPosition()[0], self.getPosition()[1], new_position[0], new_position[1])
        self.setPosition(new_position)

        return new_position
    
    def perceive(self, real_board : Board):
        i, j = self.getPosition()

        for k in range(i - 4, i + 5): # Perceive a square of size 4
            for l in range(j - 4, j + 5): # with center at agent's position
                if self.getEnv().validPosition(k, l): # If within board
                    # Update with perceived information
                    self.getEnv().setCell(k, l, real_board.getCell(k, l))

    def withinRange(self, other_agent):
        return abs(self.getPosition()[0] - other_agent.getPosition()[0]) <= 4 and \
               abs(self.getPosition()[1] - other_agent.getPosition()[1]) <= 4
    
    def receiveMessage(self, message : Board):
        size = message.getBoardSize()
        for i in range(size):
            for j in range(size):
                current_cell = self.getEnv().getCell(i, j)
                message_cell = message.getCell(i, j)

                if current_cell.isOlder(message_cell):
                    self.getEnv().setCell(i, j, message_cell)

    def message(self, other_agent):
        other_agent.receiveMessage(self.getEnv())

    def communicate(self):
        for player in self.getOtherPlayers():
            if self.withinRange(player):
                self.message(player)

    # Abstract methods

    @abc.abstractmethod
    def act(self):
        pass

    @abc.abstractmethod
    def update(self, state, action, reward, next_state):
        pass

    def __str__(self):
        return "Agent: " + str(self.__class__) + "\n" + \
                "id: " + str(self.id) + "\n" + \
               "Endowment: " + str(self.endowment) + "\n" + \
               "Utility Function: " + str(self.utility_function) + "\n"
            