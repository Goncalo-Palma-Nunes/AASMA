import abc

#######################
###    Constants    ###
#######################

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

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
    ###########################
    ###       Methods       ###
    ###########################

    def execute(self, agent, board):
        if board.takeResource(agent.getPosition()[0], agent.getPosition()[1]):
            agent.incrementEndowment()
