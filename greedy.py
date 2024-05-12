from agents import Agent, UP, DOWN, LEFT, RIGHT, SIGHT_RADIUS

class GreedyAgent(Agent):
    def __init__(self, env, endowment, utility_function=lambda x: 1):
        Agent.__init__(self, env, endowment, utility_function)


    def closestApple(self):
        i, j = self.getPosition()

        closest = None
        closest_distance = float('inf')
        size = self.getEnv().getBoardSize()
        # Iterate over the board
        for x in range(size):
            for y in range(size):
                # Check if the cell has a resource
                if self.getEnv().getCell(x, y).hasResource():
                    # Calculate the distance between the agent and the cell
                    distance = self.getEnv().manhattanDistance(i, j, x, y)
                    # If the distance is less than the closest distance, update the closest cell
                    if distance < closest_distance:
                        closest = (x, y)
                        closest_distance = distance

        return closest
    
    def act(self):
        self.perceive(self.getEnv())

        raise NotImplementedError

    def accuse(self):
        raise NotImplementedError

    def vote(self, consumption, accused):
        raise NotImplementedError

    def update(self, state, action, reward, next_state):
        raise NotImplementedError