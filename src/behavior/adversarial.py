from environment import Gather
from .cooperative import CooperativeBehavior

class AdversarialBehavior(CooperativeBehavior):
    def __init__(self, growth_frequency):
        super().__init__(growth_frequency)
        self.gather = Gather()

    def getColor(self):
        return "gold"

    def getClosestResource(self, view):
        if self.acceptableToEatMore(view):
            return super().getClosestResource(view)
        else:
            # Avoid other agents
            return view.getClosestResource(self.getPosition(), lambda i, j: not view.anyAgentsInRadius((i, j), self.getAgent().getSightRadius(), ignore=self.getPosition()))

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

    def __str__(self) -> str:
        return "Adversarial"
