from deliberative_agent import DeliberativeAgent

class CooperativeAgent(DeliberativeAgent):
    sustainable_consumption = 0

    def __init__(self, env, endowment, utility_function=lambda x: 1):
        DeliberativeAgent.__init__(self, env, endowment, utility_function)
        self.sustainable_consumption = self.computeSustainableConsumption()

    def computeSustainableConsumption(self):
        boardsize = self.getEnv().getBoardSize()
        num_players = len(self.getOtherPlayers()) + 1
        num_apples = self.getBoard().getNumApples()
        growth_frequency = self.getBoard().getResourceGrowthFrequency()

        sustainable_consumption = num_apples + (growth_frequency) * num_apples / (boardsize - num_apples)
        sustainable_consumption = sustainable_consumption / (2 * num_players)

        return sustainable_consumption
        
    def act(self):
        raise NotImplementedError("Cooperative agents must implement the act method.")
            
    def update(self, state, action, reward, next_state):
        raise NotImplementedError("Cooperative agents must implement the update method.")

    def accuse(self):
        raise NotImplementedError("Cooperative agents must implement the accuse method.")
    
    def vote(self, consumption, accused):
        raise NotImplementedError("Cooperative agents must implement the vote method.")