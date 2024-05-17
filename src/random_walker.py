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
            # print("direction is", direction)
            try:
                # print("MOVING")
                self.move(direction)
                # print("MOVED", direction)
            except ValueError as e:
                # print(e)
                # print("ERROR")
                possible_directions.remove(direction)
                direction = None

    def act(self):
        # print("Acting")
        result = self.eat()
        if result != SUCCESS:
            self.moveInRandomDirection()
            result = FAILURE
        
        return result
            
    def accuse(self):
        return random.choice(list(self.getOtherPlayers().values()))[0]

    def vote(self, consumption, accused):
        return random.choice([True, False])

    def update(self, state, action, reward, next_state):
        pass
