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

    def getSustainableConsumption(self):
        return self.sustainable_consumption
    
    def setSustainableConsumption(self, consumption):
        self.sustainable_consumption = consumption

    def moveTowardsApple(self):
        consume_apple = 0
        self.targetStillValid()
        if self.noTargetPosition() : # No current target/plan
            self.setPlan(self.pathToClosestApple())
            if self.getPlan() == []:
                # If no apples are reachable, move in a random direction
                self.moveInRandomDirection()
                self.communicate(apple_consumed=bool(consume_apple))
                return consume_apple

            self.setTargetPosition(self.getTargetFromPlan())
        else:
            # Look for a closer apple in the vicinity
            possible_new_target = self.closestAppleInRadius()
            if possible_new_target is not None:
                # If one exists, it is the closest apple and should be the target
                i, j = self.getPosition()
                x, y = possible_new_target
                self.setPlan(self.getBoard().shortestPath(i, j, x, y))
                self.setTargetPosition(self.getTargetFromPlan())

        self.move(self.positionToDirection(self.popPlan())) # Move in the direction of the next move in the plan
        if self.getPlan() == []:
        # If the plan is empty, we have reached the target position
            self.setTargetPosition(None)
            consume_apple = self.eat()

        self.communicate(apple_consumed=bool(consume_apple))
        return consume_apple
        
    def act(self):
        self.setSustainableConsumption(self.computeSustainableConsumption())

        if self.getSustainableConsumption() < self.getRoundEndowment():
            # Limit reached, move in a random direction
            self.moveInRandomDirection()
            return 0

        return self.moveTowardsApple()

    def update(self, state, action, reward, next_state):
        raise NotImplementedError("Cooperative agents must implement the update method.")

    def accuse(self):
        raise NotImplementedError("Cooperative agents must implement the accuse method.")
    
    def vote(self, consumption, accused):
        raise NotImplementedError("Cooperative agents must implement the vote method.")