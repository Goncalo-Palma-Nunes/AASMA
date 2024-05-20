from .behavior import Behavior, Plan
from environment import Gather, Move, UP, DOWN, LEFT, RIGHT, Board, Agent
from .random import RandomBehavior


import random

class CooperativeBehavior(Behavior):
    def __init__(self, growthFrequency):
        super().__init__(growthFrequency)
        self.known_agents = set()
        self.sustainable_consumption = 0
        self.plan = Plan()
        self.target_position = None

    def getColor(self):
        return "pink"

    def getPlan(self):
        return self.plan
    
    def getTargetPosition(self):
        return self.target_position
    
    def setTargetPosition(self, target_position):
        if not isinstance(target_position, (tuple, list)) \
            or not len(target_position) == 2 \
            or not all(isinstance(i, int) for i in target_position):
            raise ValueError("Target position must be a list or tuple of length 2 containing integers.")
        
        if any (i > self.getAgent().getView().getSize() for i in target_position) \
            or any (i < 0 for i in target_position):
            raise ValueError("Target position must be within the bounds of the board.")
        
        self.target_position = target_position

    def noTargetPosition(self):
        return self.getTargetPosition() is None
    
    def targetStillValid(self):
        if not self.getAgent().getView().hasResource(self.getTargetPosition()[0], 
                                         self.getTargetPosition()[1]):
            self.setTargetPosition(None)
            self.getPlan().clear()
            return False
        return True

    def computeSustainableConsumption(self, num_players : int):
        board = self.getAgent().getView()
        boardsize = board.getSize()
        num_apples = board.getNumberOfResources()
        if num_apples == 0:
            return 0 
        if num_players == 0:
            return 1
        if (boardsize - num_apples) == 0:
            # Few apples, so they should be more conservative
            sustainable_consumption = num_apples / (4 * num_players) 
            return sustainable_consumption

        sustainable_consumption = num_apples + (self.getGrowthFrequency()) * num_apples / (boardsize - num_apples)
        sustainable_consumption = sustainable_consumption / (2 * num_players)

        return sustainable_consumption

    def getSustainableConsumption(self):
        return self.sustainable_consumption
    
    def setSustainableConsumption(self, consumption):
        self.sustainable_consumption = consumption

    def moveRandomly(self):
        return Move(random.choice([UP, DOWN, LEFT, RIGHT]))

    def positionToDirection(self, position):
        # print("Position: ", position)
        # print("Current Position: ", self.getPosition())
        if position[0] < self.getPosition()[0]:
            return UP
        elif position[0] > self.getPosition()[0]:
            return DOWN
        elif position[1] < self.getPosition()[1]:
            return LEFT
        elif position[1] > self.getPosition()[1]:
            return RIGHT
        else:
            # raise ValueError("Position must be different from current position.")
            return self.moveRandomly()

        
    def moveTowardsResource(self, view : Board):
        if view.hasResource(self.getPosition()[0], self.getPosition()[1]):
            if self.getAgent().getRoundEndowment() < self.getSustainableConsumption():
                return Gather()
            else:
                return self.moveRandomly()
        
        if self.getPlan().isEmpty() or not self.targetStillValid():
            self.getPlan().definePlan(self.getAgent().pathToClosestApple())
            if self.getPlan().isEmpty():
                return self.moveRandomly()
            
            self.setTargetPosition(self.getPlan().getTarget())

        print("Plan: ", self.getPlan())
        return Move(self.positionToDirection(self.getPlan().next()))


    def act(self, view : Board, seen_actions):
        for agent, action in seen_actions:
            self.known_agents.add(agent)

        self.setSustainableConsumption(self.computeSustainableConsumption(len(self.known_agents)))

        return self.moveTowardsResource(view)


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