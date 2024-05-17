from cooperative import CooperativeAgent

#######################
###     Class       ###
#######################

class GreedyAgent(CooperativeAgent):

    ###########################
    ###     Constructor     ###
    ###########################

    def __init__(self, env, endowment, utility_function=lambda x: 1):
        CooperativeAgent.__init__(self, env, endowment, utility_function)

    ###########################
    ###     Methods         ###
    ###########################

    def act(self):
        if self.anyAgentsInRadius():
            # Mimic behaviour of cooperative agent
            return super(GreedyAgent, self).act()
        
        # otherwise move towards the closest apple
        if self.onResource():
            return self.eat()
        
        return self.moveTowardsApple()

    def accuse(self):
        raise NotImplementedError

    def vote(self, consumption, accused):
        raise NotImplementedError

    def update(self, state, action, reward, next_state):
        raise NotImplementedError