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

    def canSee(self, i, j):
        return (self.position[0] - self.sight_radius <= i <= self.position[0] + self.sight_radius and
                self.position[1] - self.sight_radius <= j <= self.position[1] + self.sight_radius)

    def incrementEndowment(self):
        self.endowment += 1
        self.roundEndowment += 1

    def pathToClosestApple(self):
        """Considers the entire view """
        return self.getView().shortestPath(self.getPosition()[0], self.getPosition()[1])

    def closestAppleInRadius(self):
        """Considers only the agent's sight radius"""
        i, j = self.getPosition()
        cell = None
        cell_distance = float('inf')
        for k in range(i - self.sight_radius, i + self.sight_radius + 1):
            for l in range(j - self.sight_radius, j + self.sight_radius + 1):
                if self.getView().hasResource(k, l) and \
                    self.getView().manhattanDistance((i, j), (k, l)) < cell_distance:
                    cell = (k, l)
                    cell_distance = self.getView().manhattanDistance((i, j), (k, l))

        return cell

    def receiveInformation(self, other):
        if self.view is not None and other.getView() is not None:
            self.view.merge(other.getView())

    def act(self, timestamp, board, seen_actions):
        # Store any seen gathers of non-surrounded resources
        for agent, action in seen_actions:
            if isinstance(action, Gather) and \
                not board.isSurroundedByResources(agent.getPosition()[0], agent.getPosition()[1]):
                self.addSeenGather(agent, agent.getPosition())

        # Update the agent's view of the board
        self.perceive(timestamp, board)

        # Pick an action to take based on the agent's behavior
        return self.behavior.act(self.view, seen_actions)

    def perceive(self, timestamp, board):
        # If the view hasn't been initialized yet, initialize it
        if self.view is None:
            self.view = Board(board.getSize())

        # Merge the visible portion of the board into the agent's view
        rect = (self.position[0] - self.sight_radius,
                self.position[1] - self.sight_radius,
                self.position[0] + self.sight_radius + 1,
                self.position[1] + self.sight_radius + 1)
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
