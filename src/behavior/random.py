from .behavior import Behavior
from environment import Gather, Move, UP, DOWN, LEFT, RIGHT

import random

class RandomBehavior(Behavior):
    def __init__(self, growthFrequency):
        super().__init__(growthFrequency)
        self.known_agents = set()

    ###########################
    ###       Methods       ###
    ###########################

    def moveRandomly(self):
        return Move(random.choice([UP, DOWN, LEFT, RIGHT])) 

    def act(self, view, seen_actions):
        for agent, action in seen_actions:
            self.known_agents.add(agent)

        i, j = self.getPosition()
        if view.hasResource(i, j):
            return Gather()

        return self.moveRandomly()

    def accuse(self):
        if self.known_agents:
            return random.choice(list(self.known_agents))
        return None

    def vote(self, accused, accused_actions):
        return random.choice([True, False])

