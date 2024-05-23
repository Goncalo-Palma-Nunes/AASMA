from math import floor
from environment import Gather, Move
from .greedy import GreedyBehavior

###########################
###      Constants      ###
###########################

class CooperativeBehavior(GreedyBehavior):
    def __init__(self, growth_frequency):
        super().__init__()
        self.growth_frequency = growth_frequency
        self.sustainable_consumption = 0

    def getColor(self):
        return "pink"

    def canEatResource(self, view, position):
        return super().canEatResource(view, position) and view.isSurroundedByResources(*position)

    def act(self, view, seen_actions):
        return super().act(view, seen_actions)

    def accuse(self):
        if self.known_agents:
            # Find agent which we saw eating the most resources which are not sustainable
            accused = None
            accused_consumption = 0
            for agent in self.known_agents:
                seen_gathers = self.getAgent().getSeenGathers(agent)
                if len(seen_gathers) > accused_consumption:
                    accused = agent
                    accused_consumption = len(seen_gathers)
            return accused
        return None

    def vote(self, accused_actions, accused):
        return len(accused_actions) > 0

    def __str__(self) -> str:
        return "Cooperative"
