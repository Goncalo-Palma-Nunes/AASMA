from agents import Agent, UP, DOWN, LEFT, RIGHT, SUCCESS, FAILURE
import random

class RandomWalker(Agent):
    def __init__(self, env, endowment, utility_function=lambda x: 0):
        Agent.__init__(self, env, endowment, utility_function)

    def moveInRandomDirection(self):
        possible_directions = [UP, DOWN, LEFT, RIGHT]
        direction = None
        while not (len(possible_directions) == 0) and direction is None:
            direction = random.choice(possible_directions)
            try:
                self.move(direction)
            except ValueError:
                possible_directions.remove(direction)
                direction = None

    def act(self):
        return self.eat() if self.eat() == SUCCESS else (self.moveInRandomDirection() or FAILURE)
            
    def accuse(self):
        return random.choice(self.getOtherPlayers())

    def vote(self, consumption, accused):
        return random.choice([True, False])

    def update(self, state, action, reward, next_state):
        pass

