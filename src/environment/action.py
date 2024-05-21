import abc
import random

#######################
###    Constants    ###
#######################

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
STAY = "stay"

class Action:
    ###########################
    ###     Attributes      ###
    ###########################

    __metaclass__ = abc.ABCMeta

    ###########################
    ###       Methods       ###
    ###########################

    @abc.abstractmethod
    def execute(self, agent, board):
        pass

class Move(Action):
    ###########################
    ###     Constructor     ###
    ###########################

    def __init__(self, direction):
        self.direction = direction

    @staticmethod
    def random():
        return Move(random.choice([UP, DOWN, LEFT, RIGHT]))

    @staticmethod
    def fromTo(from_position, to_position):
        choices = []
        if from_position[0] < to_position[0]:
            choices.append(RIGHT)
        elif from_position[0] > to_position[0]:
            choices.append(LEFT)
        if from_position[1] < to_position[1]:
            choices.append(DOWN)
        elif from_position[1] > to_position[1]:
            choices.append(UP)

        if choices:
            return Move(random.choice(choices))
        else:
            return Move.random()

    ###########################
    ###       Methods       ###
    ###########################

    def execute(self, agent, board):
        old_i, old_j = agent.getPosition()
        if self.direction == UP:
            new_i, new_j = old_i, old_j - 1
        elif self.direction == DOWN:
            new_i, new_j = old_i, old_j + 1
        elif self.direction == LEFT:
            new_i, new_j = old_i - 1, old_j
        elif self.direction == RIGHT:
            new_i, new_j = old_i + 1, old_j
        else:
            return 0

        if board.withinBounds(new_i, new_j) and not board.hasAgent(new_i, new_j):
            agent.setPosition((new_i, new_j))
            board.moveAgent(old_i, old_j, new_i, new_j)
        return 0

class Gather(Action):



    def __init__(self, acceptable=False):
        self.acceptable = acceptable
        
    ###########################
    ###       Methods       ###
    ###########################

    def isSociallyAcceptable(self):
        return self.acceptable

    def execute(self, agent, board):
        if board.takeResource(agent.getPosition()[0], agent.getPosition()[1]):
            agent.incrementEndowment()
