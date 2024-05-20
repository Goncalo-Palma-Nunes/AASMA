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

    def moveTowardsClosestResource(self, view):
        if self.target_position is None or not view.hasResource(self.target_position[0], self.target_position[1]):
            self.target_position = view.getClosestResource(self.getPosition())
            if self.target_position is None:
                return Move.random()

        return Move.fromTo(self.getPosition(), self.target_position)

    def act(self, view, seen_actions):
        for agent, action in seen_actions:
            self.known_agents.add(agent)

        if view.hasResource(self.getPosition()[0], self.getPosition()[1]):
            return Gather()

        return self.moveTowardsClosestResource(view)

    def accuse(self):
        if self.known_agents:
            # Accuse the one agent seen to have eaten more by iterating
            # through the agent's seen_gathers dictionary and comparing the
            # number of seen gathers
            accused = None
            accused_actions = -1
            for agent in self.known_agents:
                seen_gathers = self.getAgent().getSeenGathers(agent)
                if len(seen_gathers) > accused_actions:
                    accused = agent
                    accused_actions = len(seen_gathers)

            return accused
        return None

    def vote(self, accused_actions, accused):
        # Votes true if it has seen the accused agent gathering more than itself
        # print("Accused Actions: ", accused_actions)
        # print("Agent Endowment: ", self.getAgent().getRoundEndowment())
        # print("Accused: ", accused)
        # print("seen_gathers: ", len(self.getAgent().getSeenGathers(accused)))
        return len(self.getAgent().getSeenGathers(accused)) > self.getAgent().getRoundEndowment()