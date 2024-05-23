from environment import Gather
from .greedy import GreedyBehavior
from .cooperative import CooperativeBehavior

class AdversarialBehavior(CooperativeBehavior):
    def __init__(self, growth_frequency):
        super().__init__(growth_frequency)
        self.gather = Gather()

    def getColor(self):
        return "gold"

    def canEatResource(self, view, position):
        if super().canEatResource(view, position):
            return True
        return not view.anyAgentsInRadius(position, self.getAgent().getSightRadius(), ignore=self.getPosition())

    def act(self, view, seen_actions):
        return GreedyBehavior.act(self, view, seen_actions)

    def accuse(self):
        return GreedyBehavior.accuse(self)

    def vote(self, accused_actions, accused):
        return GreedyBehavior.vote(self, accused_actions, accused)

    def __str__(self) -> str:
        return "Adversarial"
