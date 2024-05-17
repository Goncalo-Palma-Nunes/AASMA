from .behavior import Behavior
from environment import Gather, Move, UP, DOWN, LEFT, RIGHT

import random

class RandomBehavior(Behavior):
    def __init__(self):
        super().__init__()
        self.known_agents = set()

    ###########################
    ###       Methods       ###
    ###########################

    def act(self, view, seen_actions):
        for agent, action in seen_actions:
            self.known_agents.add(agent)

        i, j = self.getPosition()
        if view.hasResource(i, j):
            return Gather()

        return Move(random.choice([UP, DOWN, LEFT, RIGHT]))

    def accuse(self):
        if self.known_agents:
            return random.choice(list(self.known_agents))
        return None

    def vote(self, accused, accused_actions):
        return random.choice([True, False])
