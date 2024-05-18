from environment import Gather, UP, DOWN, LEFT, RIGHT, Move
from .random import RandomBehavior
from .cooperative import CooperativeBehavior
from environment.agent import Agent
from environment.board import Board

import random

class GreedyBehavior(CooperativeBehavior):
    def __init__(self, growthFrequency):
        super().__init__(growthFrequency)
        self.gather = Gather()

    def anyAgentsInRadius(self):
        i, j = self.getPosition()
        radius = self.getAgent().getSightRadius()
        for k in range(i - radius, i + radius + 1):
            for l in range(j - radius, j + radius + 1):
                if self.getAgent().getView().withinBounds(k, l) and \
                    self.getAgent().getView().hasAgent(k, l):
                    return True
        return False

    def act(self, view, seen_actions):
        for agent, action in seen_actions:
            self.known_agents.add(agent)

        if self.anyAgentsInRadius():
            return super().act(view, seen_actions)
        
        if view.hasResource(self.getPosition()[0], self.getPosition()[1]):
            return Gather()
        
        if self.getPlan().isEmpty() or not self.targetStillValid():
            self.getPlan().definePlan(self.getAgent().pathToClosestApple())
            if self.getPlan().isEmpty():
                return RandomBehavior.moveRandomly()
            
            self.setTargetPosition(self.getPlan().getTarget())

        return Move(self.positionToDirection(self.getPlan().next()))

    def accuse(self):
        return super().accuse()

    def vote(self, accused, accused_actions):
        return None
