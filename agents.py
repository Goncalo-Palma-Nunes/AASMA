import abc
from board import Board
import itertools

#######################
###    Constants    ###
#######################

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
SUCCESS = 1
FAILURE = 0
SIGHT_RADIUS = 4


#######################
###     Class       ###
#######################

class Agent:

    ###########################
    ###       Attributes    ###
    ###########################

    __metaclass__ = abc.ABCMeta
    id = itertools.count()

    ###########################
    ###     Constructor     ###
    ###########################
    
    def __init__(self, env : Board, endowment, utility_function, position=None,
                  other_players=[], timestamp=0):
        self.setTimeStamp(timestamp)
        self.setEnv(env)
        self.setEndowment(endowment)
        self.setUtilityFunction(utility_function)
        self.id = next(self.id)
        self.other_players = dict()
        self.setOtherPlayers(other_players)
        self.position = position

    ###########################
    ### Getters and setters ###
    ###########################

    def getId(self):
        return self.id

    def getEnv(self):
        return self.env
    
    def getEndowment(self):
        return self.endowment
    
    def getPosition(self):
        return self.position
    
    def getOtherPlayers(self):
        return self.other_players
    
    def getTimeStamp(self):
        return self.timestamp
    
    def getOtherPlayer(self, id):
        return self.getOtherPlayers()[id][0]
    
    def getOtherPlayerTimestamp(self, id):
        return self.getOtherPlayers()[id][2]
    
    def getOtherPlayerResources(self, id):
        return self.getOtherPlayers()[id][1]
    
    def getId(self):
        return self.id
    
    def getPlayer(self, id):
        return self.getOtherPlayers()[id][0]
    
    def getPlayerResources(self, id):
        return self.getOtherPlayers()[id][1]
    
    def utilityFunction(self):
        return self.utility_function
    
    def setEnv(self, env):
        if not isinstance(env, Board):
            raise ValueError("Environment must be of type Board.")
        self.env = env

    def setTimeStamp(self, timestamp):
        self.timestamp = timestamp

    def setEndowment(self, endowment):
        self.endowment = endowment

    def setUtilityFunction(self, utility_function):
        if not callable(utility_function):
            raise ValueError("Utility function must be a callable function.")
        
        self.utility_function = utility_function

    def setPosition(self, position):
        if not isinstance(position, tuple) or len(position) != 2:
            raise ValueError("Position must be a tuple of length 2.")
        if any (i > self.getEnv().getBoardSize() for i in position):
            raise ValueError("Position must be within the bounds of the board.")
        self.position = position

    def setOtherPlayers(self, other_players):
        if not isinstance(other_players, (list, tuple)):
            raise ValueError("Other players must be a list or tuple.")
        for player in other_players:
            if not isinstance(player, Agent):
                raise ValueError("Other players must be of type Agent.")
            self.addOtherPlayer(player)

    def addOtherPlayer(self, player, resources=0, timestamp=0):
        if not isinstance(player, Agent):
            raise ValueError("Player must be of type Agent.")
        self.other_players[player.getId()] = [player, resources, timestamp]

    def updateOtherPlayerResources(self, id, resources):
        self.getOtherPlayers()[id][1] = resources

    def updateOtherPlayerTimeStamp(self, id, timestamp):
        self.getOtherPlayers()[id][2] = timestamp

    def incrementOtherPlayerTimeStamp(self, id):
        self.getOtherPlayers()[id][2] += 1

    ###########################
    ###     Environment     ###
    ### Interaction Methods ###
    ###########################

    def onResource(self):
        return self.getEnv().hasResource(self.getPosition()[0], self.getPosition()[1])
    
    def __validateMove(self, direction):
        new_position = self.getPosition()
        if direction == UP:
            new_position = (self.getPosition()[0] + 1, self.getPosition()[1])
        elif direction == DOWN:
            new_position = (self.getPosition()[0] - 1, self.getPosition()[1])
        elif direction == LEFT:
            new_position = (self.getPosition()[0], self.getPosition()[1] - 1)
        elif direction == RIGHT:
            new_position = (self.getPosition()[0], self.getPosition()[1] + 1)
        else:
            raise ValueError("Invalid direction. Must be 'up', 'down', 'left', or 'right'.")
        
        if not self.getEnv().validPosition(new_position[0], new_position[1]):
            raise ValueError("Cannot move out of bounds.")
        if not self.getEnv().noAgent(new_position[0], new_position[1]):
            raise ValueError("Cannot move to a position with another agent.")
        
        return new_position

    def eat(self):
        if self.onResource():
            self.setEndowment(self.getEndowment() + 1)
            self.getEnv().removeResource(self.getPosition()[0], self.getPosition()[1])
            return SUCCESS
        return FAILURE
    
    def move(self, direction):
        new_position = self.__validateMove(direction)
        
        self.getEnv().moveAgent(self.getPosition()[0], self.getPosition()[1], new_position[0], new_position[1])
        self.setPosition(new_position)

        return new_position
    
    def perceive(self, real_board : Board):
        i, j = self.getPosition()

        for k in range(i - SIGHT_RADIUS, i + SIGHT_RADIUS + 1): # Perceive a square of size SIGHT_RADIUS
            for l in range(j - SIGHT_RADIUS, j + SIGHT_RADIUS + 1): # with center at agent's position
                if self.getEnv().validPosition(k, l): # If within board
                    # Update with perceived information
                    self.getEnv().setCell(k, l, real_board.getCell(k, l))

    ############################
    ###    Communication     ###
    ###       Methods        ###
    ############################

    def withinRange(self, other_agent):
        return abs(self.getPosition()[0] - other_agent.getPosition()[0]) <= 4 and \
               abs(self.getPosition()[1] - other_agent.getPosition()[1]) <= 4
    
    def processNewBoard(self, new_board : Board):
        size = new_board.getBoardSize()
        for i in range(size):
            for j in range(size):
                current_cell = self.getEnv().getCell(i, j)
                new_board_cell = new_board.getCell(i, j)

                if current_cell.isOlder(new_board_cell):
                    self.getEnv().setCell(i, j, new_board_cell)

    def processPlayerInfo(self, other_players : dict):
        for key, value in other_players.items():
            received_timestamp = value[2]
            received_resources = value[1]

            current_timestamp = self.getOtherPlayerTimestamp(key)
            current_resources = self.getOtherPlayerResources(key)

            if received_timestamp > current_timestamp or \
                received_resources > current_resources:
                self.updateOtherPlayerResources(key, received_resources)
                self.updateOtherPlayerTimeStamp(key, received_timestamp)

    
    def receiveMessage(self, message : Board, other_players : dict, id : int, apple_consumed : bool = False):
        self.processNewBoard(message)
        self.processPlayerInfo(other_players)

        if apple_consumed:
            self.incrementOtherPlayerTimeStamp(id)


    def message(self, other_agent, apple_consumed : bool = False):
        other_agent.receiveMessage(self.getEnv(), self.getOtherPlayers(),
                                   self.getId(), apple_consumed)

    def communicate(self, apple_consumed : bool):
        for value in self.getOtherPlayers().values():
            player = value[0]
            if self.withinRange(player):
                self.message(player)

    def disclose_consumption(self, accused):
        return {} # TODO

    ############################
    ###        Abstract      ###
    ###        Methods       ###
    ############################


    @abc.abstractmethod
    def act(self):
        pass

    @abc.abstractmethod
    def accuse(self):
        pass

    @abc.abstractmethod
    def vote(self, consumption, accused):
        pass

    @abc.abstractmethod
    def update(self, state, action, reward, next_state):
        pass


    ############################
    ###      Magic Methods   ###
    ############################

    def __str__(self):
        return "Agent: " + str(self.__class__) + "\n" + \
                "id: " + str(self.id) + "\n" + \
               "Endowment: " + str(self.endowment) + "\n" + \
               "Utility Function: " + str(self.utility_function) + "\n"
    
    def __eq__(self, other):
        if not isinstance(other, Agent):
            return False

        return self.getId() == other.getId()
            