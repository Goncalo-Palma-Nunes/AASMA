from math import floor
from environment import Gather, Move
from .greedy import GreedyBehavior

###########################
###      Constants      ###
###########################

# The growth cooperative agents should aim for, as a fraction of the ideal growth.
IDEAL_GROWTH_FACTOR = 0.8

# The fraction of the growth that can be consumed even when the growth is less than the ideal growth.
SUSTAINABLE_CONSUMPTION_FRACTION = 0.2

class CooperativeBehavior(GreedyBehavior):
    def __init__(self, growth_frequency):
        super().__init__()
        self.growth_frequency = growth_frequency
        self.sustainable_consumption = 0

    def getColor(self):
        return "pink"

    def computeSustainableConsumption(self, view):
        # Count the number of resources
        resource_count = view.getResourceCount()

        # Estimate the number of resources that will grow next round
        growth = view.estimateResourceGrowth(self.growth_frequency)
        
        # Estimate the ideal growth of resources.
        (ideal_growth, ideal_count) = view.getIdealResourceGrowthAndCount(self.growth_frequency)

        if growth < IDEAL_GROWTH_FACTOR * ideal_growth:
            # If the growth is less than the ideal growth, then the population should only eat a fraction of the growth.
            sustainable_consumption = growth * SUSTAINABLE_CONSUMPTION_FRACTION
        else:
            # Otherwise, its safe to consume all the growth.
            sustainable_consumption = growth

        # Allow eating excess resources.
        sustainable_consumption += max(0, resource_count - ideal_count)

        # We return the sustainable consumption per agent.
        self.sustainable_consumption = floor(sustainable_consumption / (len(self.getKnownAgents()) + 1))
        return self.sustainable_consumption

    def acceptableToEatMore(self, view):
        sustainable_consumption = self.computeSustainableConsumption(view)
        return self.getAgent().getRoundEndowment() < sustainable_consumption

    def getClosestResource(self, view):
        if self.acceptableToEatMore(view):
            return super().getClosestResource(view)
        else:
            return view.getClosestResource(self.getPosition(), lambda i, j: view.hasSurroundedResource(i, j))

    def act(self, view, seen_actions):
        for agent, action in seen_actions:
            self.known_agents.add(agent)

        if view.hasResource(self.getPosition()[0], self.getPosition()[1]):
            sustainable_consumption = self.computeSustainableConsumption(view)
            if self.acceptableToEatMore(view):
                return Gather()
            elif view.hasSurroundedResource(self.getPosition()[0], self.getPosition()[1]):
                # Socially acceptable to eat more than sustainable consumption if the resource is surrounded
                return Gather(acceptable=True)
            else:
                return Move.random()

        return self.moveTowardsClosestResource(view)

    def accuse(self):
        if self.known_agents:
            # Find agent which we saw eating the most
            accused = None
            accused_consumption = -1
            for agent in self.known_agents:
                seen_gathers = self.getAgent().getSeenGathers(agent)
                if len(seen_gathers) > accused_consumption:
                    accused = agent
                    accused_consumption = len(seen_gathers)

            # Accuse agent if it consumed more than the sustainable consumption and more than ourselves
            if accused is not None and accused_consumption > self.sustainable_consumption and accused_consumption > self.getAgent().getRoundEndowment():
                    return accused
        return None

    def vote(self, accused_actions, accused):
        return super().vote(accused_actions, accused)
