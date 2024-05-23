import itertools

from .board import Board
from .action import Gather

class Agent:
    ###########################
    ###      Attributes     ###
    ###########################

    id = itertools.count()

    ###########################
    ###     Constructor     ###
    ###########################

    def __init__(self, behavior, position, sight_radius):
        self.id = next(Agent.id)
        self.behavior = behavior
        self.position = position
        self.sight_radius = sight_radius

        self.behavior.setAgent(self)

        self.endowment = 0
        self.roundEndowment = 0
        self.view = None
        self.seen_gathers = {}
        self.imprisoned = False

    ###########################
    ### Getters and setters ###
    ###########################

    def imprison(self):
        self.imprisoned = True

    def isImprisoned(self):
        return self.imprisoned

    def getId(self):
        return self.id
    
    def getRoundEndowment(self):
        return self.roundEndowment
    
    def getBehavior(self):
        return self.behavior

    def getColor(self):
        return self.behavior.getColor()
    
    def getView(self):
        return self.view

    def getEndowment(self):
        return self.endowment

    def getPosition(self):
        return self.position

    def setPosition(self, position):
        self.position = position

    def setRoundEndowment(self, endowment):
        self.roundEndowment = endowment

    def getSightRadius(self):
        return self.sight_radius

    def getSeenGathers(self, accused):
        return self.seen_gathers.get(accused, set())

    ###########################
    ###       Methods       ###
    ###########################
    
    def addSeenGather(self, accused, position):
        self.seen_gathers.setdefault(accused, set()).add(position)

    def couldSee(self, from_i, from_j, i, j):
        return (from_i - self.sight_radius <= i <= from_i + self.sight_radius and
                from_j - self.sight_radius <= j <= from_j + self.sight_radius)

    def canSee(self, i, j):
        return self.couldSee(self.position[0], self.position[1], i, j)

    def incrementEndowment(self):
        self.endowment += 1
        self.roundEndowment += 1

    def receiveInformation(self, other):
        if self.view is not None and other.getView() is not None:
            self.view.merge(other.getView())

    def act(self, board, seen_actions):
        # Store any seen gathers of non-surrounded resources
        for agent, action in seen_actions:
            if isinstance(action, Gather) and \
                not board.isSurroundedByResources(*agent.getPosition()):
                self.addSeenGather(agent, agent.getPosition())

        # Update the agent's view of the board
        self.perceive(board)

        # Pick an action to take based on the agent's behavior
        return self.behavior.act(self.view, seen_actions)

    def perceive(self, board):
        # If the view hasn't been initialized yet, initialize it
        if self.view is None:
            self.view = Board(board.getSize())

        # Merge the visible portion of the board into the agent's view
        rect = (self.position[0] - self.sight_radius,
                self.position[1] - self.sight_radius,
                self.position[0] + self.sight_radius,
                self.position[1] + self.sight_radius)
        self.view.merge(board, rect)

    def accuse(self):
        return self.behavior.accuse()

    def vote(self, accused, accused_actions):
        return self.behavior.vote(accused, accused_actions)

    ###########################
    ###     Overridden      ###
    ###########################

    def __hash__(self):
        return hash(self.id)
