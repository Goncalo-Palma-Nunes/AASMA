import abc

class Behavior:
    ###########################
    ###     Attributes      ###
    ###########################

    __metaclass__ = abc.ABCMeta

    ###########################
    ###     Constructor     ###
    ###########################

    def __init__(self):
        self.agent = None

    ###########################
    ### Getters and Setters ###
    ###########################

    def setAgent(self, agent):
        if self.agent is not None:
            raise ValueError("This behavior is already assigned to an agent.")
        self.agent = agent

    def getAgent(self):
        return self.agent

    def getPosition(self):
        return self.agent.getPosition()

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
