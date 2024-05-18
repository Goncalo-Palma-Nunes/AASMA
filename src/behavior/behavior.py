import abc
from src.environment.agent import Agent
from src.environment.action import Action

class Behavior:
    ###########################
    ###     Attributes      ###
    ###########################

    __metaclass__ = abc.ABCMeta

    ###########################
    ###     Constructor     ###
    ###########################

    def __init__(self, growthFrequency):
        self.agent = None
        self.growthFrequency = growthFrequency

    ###########################
    ### Getters and Setters ###
    ###########################

    def setAgent(self, agent : Agent):
        if self.agent is not None:
            raise ValueError("This behavior is already assigned to an agent.")
        self.agent = agent

    def setGrowthFrequency(self, growthFrequency):
        self.growthFrequency = growthFrequency

    def getAgent(self):
        return self.agent

    def getPosition(self):
        return self.agent.getPosition()
    
    def getGrowthFrequency(self):
        return self.growthFrequency

    ###########################
    ###       Methods       ###
    ###########################

    @abc.abstractmethod
    def act(self, view, seen_actions):
        pass

    @abc.abstractmethod
    def accuse(self):
        pass

    @abc.abstractmethod
    def vote(self, accused, accused_actions):
        pass

class Plan:
    ###########################
    ###     Constructor     ###
    ###########################

    def __init__(self):
        self.plan = []

    ###########################
    ###       Methods       ###
    ###########################

    def add(self, action : Action):
        self.plan.append(action)

    def first(self):
        return self.plan[0]
    
    def next(self):
        self.plan.pop(0)

    def definePlan(self, plan : list):
        self.plan = plan

    def clear(self):
        self.plan = []

    def isEmpty(self):
        return len(self.plan) == 0
    
    def getTarget(self):
        return self.plan[-1]