from environment import Gather, Move
from .greedy import GreedyBehavior

class CooperativeBehavior(GreedyBehavior):
    def __init__(self, growth_frequency):
        super().__init__()
        self.growth_frequency = growth_frequency

    def getColor(self):
        return "pink"

    def computeSustainableConsumption(self, view):
        num_resources = view.getNumberOfResources()
        num_agents = len(self.getKnownAgents())

        if num_resources == 0:
            return 0 
        if num_agents == 0:
            return 1
        if (view.getSize() - num_resources) == 0:
            # Few resources, so they should be more conservative
            sustainable_consumption = num_resources / (4 * num_agents) 
            return sustainable_consumption

        sustainable_consumption = num_resources + self.growth_frequency * num_resources / (view.getSize() - num_resources)
        sustainable_consumption = sustainable_consumption / (2 * num_agents)

        return sustainable_consumption

    def act(self, view, seen_actions):
        for agent, action in seen_actions:
            self.known_agents.add(agent)

        if view.hasResource(self.getPosition()[0], self.getPosition()[1]):
            sustainable_consumption = self.computeSustainableConsumption(view)
            if self.getAgent().getRoundEndowment() < sustainable_consumption:
                return Gather()
            else:
                return Move.random()

        return self.moveTowardsClosestResource(view)

    def accuse(self):
        return super().accuse()

    def vote(self, accused_actions, accused):
        return super().vote(accused_actions, accused)
