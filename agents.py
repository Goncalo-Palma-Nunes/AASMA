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
    

    def __init__(self, env, endowment, utility_function, position=None):
        self.setEnv(env)
        self.setEndowment(endowment)
        self.setUtilityFunction(utility_function)
        self.id = next(self.id)
        self.position = position

    def getEnv(self):
        return self.env
    
    def getEndowment(self):
        return self.endowment
    
    def getPosition(self):
        return self.position
    
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

    @abc.abstractmethod
    def act(self):
        pass

    @abc.abstractmethod
    def update(self, state, action, reward, next_state):
        pass

    def __str__(self):
        return "Agent: " + str(self.__class__) + "\n" + \
               "Env: " + str(self.env) + "\n" + \
               "Endowment: " + str(self.endowment) + "\n" + \
               "Utility Function: " + str(self.utility_function) + "\n"
            