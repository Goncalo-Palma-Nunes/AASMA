from random_walker import RandomWalker

class DeliberativeAgent(RandomWalker):

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
        self.setPlan([])
        self.setTargetPosition(None)

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
        raise NotImplementedError("Deliberative agents must implement the act method.")
            
    def update(self, state, action, reward, next_state):
        raise NotImplementedError("Deliberative agents must implement the update method.")

    def accuse(self):
        raise NotImplementedError("Deliberative agents must implement the accuse method.")
    
    def vote(self, consumption, accused):
        raise NotImplementedError("Deliberative agents must implement the vote method.")