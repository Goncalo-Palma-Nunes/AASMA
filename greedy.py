from agents import Agent, UP, DOWN, LEFT, RIGHT
from random_walker import RandomWalker
import random

#######################
###     Class       ###
#######################

class GreedyAgent(RandomWalker):

    ###########################
    ###       Attributes    ###
    ###########################

    target_position = None
    plan = []

    ###########################
    ###     Constructor     ###
    ###########################

    def __init__(self, env, endowment, utility_function=lambda x: 1):
        RandomWalker.__init__(self, env, endowment, utility_function)

    ###########################
    ### Getters and setters ###
    ###########################

    def getTargetPosition(self):
        return self.target_position
    
    def setTargetPosition(self, target_position):
        if not isinstance(target_position, (tuple, list)) \
            or not len(target_position) == 2 \
            or not all(isinstance(i, int) for i in target_position):
            raise ValueError("Target position must be a list or tuple of length 2 containing integers.")
        
        if any (i > self.getEnv().getBoardSize() for i in target_position) \
            or any (i < 0 for i in target_position):
            raise ValueError("Target position must be within the bounds of the board.")
        
        self.target_position = target_position

    def getPlan(self):
        return self.plan
    
    def setPlan(self, plan):
        if not isinstance(plan, list):
            raise ValueError("Plan must be a list.")
        self.plan = plan

    def nextMove(self):
        return self.getPlan()[0]
    
    def getTargetFromPlan(self):
        return self.getPlan()[-1]

    def popPlan(self):
        return self.getPlan().pop(0)
    
    
    ###########################
    ###     Methods         ###
    ###########################

    def noTargetPosition(self):
        return self.getTargetPosition() is None
    
    def targetStillValid(self):
        if not self.getBoard().hasResource(self.getTargetPosition()[0], 
                                         self.getTargetPosition()[1]):
            self.setTargetPosition(None)
            self.setPlan([])
            return False
        return True

    def act(self):
        self.perceive(self.getEnv())
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