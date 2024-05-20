from environment import Gather
from .cooperative import CooperativeBehavior

class AdversarialBehavior(CooperativeBehavior):
    def __init__(self, growthFrequency):
        super().__init__(growthFrequency)
        self.gather = Gather()

    def getColor(self):
        return "gold"

    def act(self, view, seen_actions):
        for agent, action in seen_actions:
            self.known_agents.add(agent)

        if view.hasResource(self.getPosition()[0], self.getPosition()[1]):
            if not view.anyAgentsInRadius(self.getPosition(), self.getAgent().getSightRadius()):
                return Gather()

        return super().act(view, seen_actions)

    def accuse(self):
        return super().accuse()

    def vote(self, accused_actions, accused):
        return super().vote(accused_actions, accused)
