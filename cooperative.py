from deliberative_agent import DeliberativeAgent

class CooperativeAgent(DeliberativeAgent):
    def __init__(self, env, endowment, utility_function=lambda x: 1):
        DeliberativeAgent.__init__(self, env, endowment, utility_function)
        self.setPlan([])
        self.setTargetPosition(None)
        
    def act(self):
        raise NotImplementedError("Cooperative agents must implement the act method.")
            
    def update(self, state, action, reward, next_state):
        raise NotImplementedError("Cooperative agents must implement the update method.")

    def accuse(self):
        raise NotImplementedError("Cooperative agents must implement the accuse method.")
    
    def vote(self, consumption, accused):
        raise NotImplementedError("Cooperative agents must implement the vote method.")