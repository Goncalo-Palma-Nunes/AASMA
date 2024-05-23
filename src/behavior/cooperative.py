from math import floor
from environment import Gather, Move, STAY
from .greedy import GreedyBehavior

###########################
###      Constants      ###
###########################

PROTECT_RESOURCE_THRESHOLD = 10

class CooperativeBehavior(GreedyBehavior):
    def __init__(self, resource_frequency, growth_frequency):
        super().__init__()
        self.resource_frequency = resource_frequency
        self.growth_frequency = growth_frequency
        self.sustainable_consumption = 0

    def getColor(self):
        return "pink"

    def canEatResource(self, view, position):
        return super().canEatResource(view, position) and view.isSurroundedByResources(*position) and \
               not any(view.hasAgent(*position) and position != self.getPosition() for position in view.getNeighbors(*position))

    def act(self, view, seen_actions):
        for agent, action in seen_actions:
            self.known_agents.add(agent)

        if view.hasResource(*self.getPosition()) and self.canEatResource(view, self.getPosition()):
            return Gather()

        move = self.moveTowardsClosestResource(view)
        if move is None:
            # There are no sustainable resources left.
            if view.estimateResourceCount(self.resource_frequency) < PROTECT_RESOURCE_THRESHOLD:
                # There are very few resources, so we'll try to protect them from non-cooperative agents.
                # Find the closest non-occupied resource and stay there.
                if view.hasResource(*self.getPosition()):
                    move = Move(STAY)
                else:
                    closest_resource = view.getClosestResource(self.getPosition(), lambda i, j: not view.hasAgent(i, j))
                    if closest_resource is not None:
                        move = Move.fromTo(self.getPosition(), closest_resource)

            if move is None:
                # There are enough resources so that we can afford to explore (or all resources are occupied).
                move = self.moveTowardsUnseenPosition(view)
        return self.checkMove(view, move)

    def accuse(self):
        return super().accuse()

    def vote(self, accused_actions, accused):
        return len(accused_actions) > 0 and accused != self.getAgent()

    def __str__(self) -> str:
        return "Cooperative"
