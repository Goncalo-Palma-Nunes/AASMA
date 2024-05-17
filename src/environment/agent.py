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
        self.view = None
        self.seen_gathers = {}

    ###########################
    ### Getters and setters ###
    ###########################

    def getId(self):
        return self.id
    
    def getBehavior(self):
        return self.behavior

    def getEndowment(self):
        return self.endowment

    def getPosition(self):
        return self.position

    def setPosition(self, position):
        self.position = position

    def getSeenGathers(self, accused):
        return self.seen_gathers.get(accused, set())

    ###########################
    ###       Methods       ###
    ###########################

    def canSee(self, i, j):
        return (self.position[0] - self.sight_radius <= i <= self.position[0] + self.sight_radius and
                self.position[1] - self.sight_radius <= j <= self.position[1] + self.sight_radius)

    def incrementEndowment(self):
        self.endowment += 1

    def act(self, timestamp, board, seen_actions):
        # Store any seen gathers
        for agent, action in seen_actions:
            if isinstance(action, Gather):
                seen_gathers = self.seen_gathers.get(agent, set())
                seen_gathers.add((agent.getPosition()[0], agent.getPosition()[1]))

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
