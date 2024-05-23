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
            return Move(STAY)

    ###########################
    ### Getters and Setters ###
    ###########################

    def isStay(self):
        return self.direction == STAY

    def getNextPosition(self, old_i, old_j):
        if self.direction == UP:
            return old_i, old_j - 1
        elif self.direction == DOWN:
            return old_i, old_j + 1
        elif self.direction == LEFT:
            return old_i - 1, old_j
        elif self.direction == RIGHT:
            return old_i + 1, old_j
        else:
            return old_i, old_j

    ###########################
    ###       Methods       ###
    ###########################

    def execute(self, agent, board):
        old_i, old_j = agent.getPosition()
        new_i, new_j = self.getNextPosition(old_i, old_j)
        if board.isFreeToMove(new_i, new_j):
            agent.setPosition((new_i, new_j))
            board.moveAgent(old_i, old_j, new_i, new_j)

class Gather(Action):
    ###########################
    ###       Methods       ###
    ###########################

    def execute(self, agent, board):
        if board.takeResource(*agent.getPosition()):
            agent.incrementEndowment()
