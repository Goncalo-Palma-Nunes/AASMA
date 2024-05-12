from agents import Agent, UP, DOWN, LEFT, RIGHT

class GreedyAgent(Agent):
    def __init__(self, env, endowment, utility_function=lambda x: 1):
        Agent.__init__(self, env, endowment, utility_function)
    
    def act(self):
        raise NotImplementedError

    def accuse(self):
        raise NotImplementedError

    def vote(self, consumption, accused):
        raise NotImplementedError

    def update(self, state, action, reward, next_state):
        raise NotImplementedError