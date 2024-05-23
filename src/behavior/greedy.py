from environment import Gather, Move
from .behavior import Behavior, Plan

class GreedyBehavior(Behavior):
    def __init__(self):
        super().__init__()
        self.known_agents = set()
        self.plan = Plan()
        self.target_position = None

    def getColor(self):
        return "purple"

    def getKnownAgents(self):
        return self.known_agents

    def canEatResource(self, view, position):
        return not view.hasAgent(*position) or position == self.getPosition()

    def moveTowardsClosestResource(self, view):
        if self.target_position is None or not view.hasResource(*self.target_position) or not self.canEatResource(view, self.target_position):
            self.target_position = view.getClosestResource(self.getPosition(), lambda i, j: self.canEatResource(view, (i, j)))
            if self.target_position is None:
                return None

        return Move.fromTo(self.getPosition(), self.target_position)

    def moveTowardsUnseenPosition(self, view):
        return Move.fromTo(self.getPosition(), view.getOldestPosition())

    def checkMove(self, view, move):
        if move is not None:
            if move.isStay() or view.isFreeToMove(*move.getNextPosition(*self.getPosition())):
                return move
        return Move.random()

    def act(self, view, seen_actions):
        for agent, action in seen_actions:
            self.known_agents.add(agent)

        if view.hasResource(*self.getPosition()) and self.canEatResource(view, self.getPosition()):
            return Gather()

        return self.checkMove(view, self.moveTowardsClosestResource(view) or self.moveTowardsUnseenPosition(view))

    def accuse(self):
        if self.known_agents:
            # Find agent which we saw eating the most resources which are not sustainable
            accused = None
            accused_consumption = 0
            for agent in self.known_agents:
                if not agent.isImprisoned():
                    seen_gathers = self.getAgent().getSeenGathers(agent)
                    if len(seen_gathers) > accused_consumption:
                        accused = agent
                        accused_consumption = len(seen_gathers)
            return accused
        return None

    def vote(self, consumption, accused):
        # Votes true if it has seen the accused agent gathering more than itself
        if accused == self.getAgent():
            return False
        return len(consumption) > self.getAgent().getRoundEndowment()
    
    def __str__(self) -> str:
        return "Greedy"
