from agents import Agent, UP, DOWN, LEFT, RIGHT
import random

class RandomWalker(Agent):
    def __init__(self, env, endowment, utility_function=lambda x: 0):
        Agent.__init__(self, env, endowment, utility_function)
    
    def act(self):
        if self.onResource():
            self.setEndowment(self.getEndowment() + 1)
            self.getEnv().removeResource(self.getPosition()[0], self.getPosition()[1])
            return 1
        
        possible_directions = [UP, DOWN, LEFT, RIGHT]
        direction = None
        while not (len(possible_directions) == 0) and direction is None:
            direction = random.choice(possible_directions)
            try:
                self.move(direction)
            except ValueError:
                possible_directions.remove(direction)
                direction = None
            
        return 0

    def update(self, state, action, reward, next_state):
        pass

