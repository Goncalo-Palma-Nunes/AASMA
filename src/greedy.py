from deliberative_agent import DeliberativeAgent

#######################
###     Class       ###
#######################

class GreedyAgent(DeliberativeAgent):

    ###########################
    ###     Constructor     ###
    ###########################

    def __init__(self, env, endowment, utility_function=lambda x: 1):
        DeliberativeAgent.__init__(self, env, endowment, utility_function)

    ###########################
    ###     Methods         ###
    ###########################

    def act(self):
        consume_apple = False
        self.targetStillValid()

        if self.noTargetPosition() : # No current target/plan
            self.setPlan(self.pathToClosestApple())
            if self.getPlan() == []:
                # If no apples are reachable, move in a random direction
                self.moveInRandomDirection()
                self.communicate(apple_consumed=consume_apple)
                return

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
            consume_apple = bool(self.eat())

        self.communicate(apple_consumed=consume_apple)

    def accuse(self):
        raise NotImplementedError

    def vote(self, consumption, accused):
        raise NotImplementedError

    def update(self, state, action, reward, next_state):
        raise NotImplementedError