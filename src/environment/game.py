from .agent import Agent
from .board import Board

from math import floor
from random import random

class Game:
    ###########################
    ###     Constructor     ###
    ###########################

    def __init__(self, board_size, behaviors, sight_radius, resource_frequency, resource_growth_frequency, num_rounds, num_turns):
        self.board = Board(board_size)
        self.agents = []
        self.num_rounds = num_rounds
        self.num_turns = num_turns
        self.resource_growth_frequency = resource_growth_frequency

        # Create agents from the behaviors
        if board_size ** 2 < len(behaviors):
            raise ValueError("Number of agents must be less than or equal to the board size squared.")
        free_positions = [(i, j) for i in range(board_size) for j in range(board_size)]
        for behavior in behaviors:
            # Pick a random free position in the board.
            i = floor(random() * len(free_positions))
            position = free_positions.pop(i)

            # Create agent and place it in the board.
            agent = Agent(behavior, position, sight_radius)
            self.agents.append(agent)
            self.board.putAgent(position[0], position[1], agent)
        self.actions = []

        # Generate initial resources
        self.board.generateResources(resource_frequency)

        self.current_round = 0
        self.current_turn = 0
        self.done = False
        self.accusations = {}
        self.votes = {}
        self.imprisoned = None

    ###########################
    ### Getters and setters ###
    ###########################

    def getBoard(self):
        return self.board
        
    def getBoardSize(self):
        return self.getBoard().getSize()
    
    def getAgents(self):
        return self.agents

    def getNumRounds(self):
        return self.num_rounds
    
    def getNumTurns(self):
        return self.num_turns

    def getCurrentRound(self):
        return self.current_round
    
    def getCurrentTurn(self):
        return self.current_turn

    def getAccusations(self):
        return self.accusations

    def getVotes(self):
        return self.votes

    def getDone(self):
        return self.done

    def getImprisoned(self):
        return self.imprisoned

    def getResourceGrowthFrequency(self):
        return self.resource_growth_frequency

    ###########################
    ###       Methods       ###
    ###########################

    def getTotalReward(self):
        return sum(agent.getEndowment() for agent in self.getAgents())

    def getMostAccused(self):
        max_count = 0
        most_accused = None
        accusation_count = {}
        for accused in self.getAccusations().values():
            if accused in accusation_count:
                accusation_count[accused] += 1
            else:
                accusation_count[accused] = 1
            if accusation_count[accused] > max_count:
                max_count = accusation_count[accused]
                most_accused = accused
        return most_accused
    
    def getOrderedAccusedList(self):
        accusation_count = {}
        for player in self.getAgents():
            accusation_count[player] = 0
        for accused in self.getAccusations().values():
            if accused in accusation_count:
                accusation_count[accused] += 1
            else:
                accusation_count[accused] = 1
        return {k: v for k, v in sorted(accusation_count.items(), key=lambda item: item[1], reverse=True)}
    
    def getMostVoted(self):
        max_count = 0
        most_voted = None
        for agent, count in self.getVotes().items():
            if count > max_count:
                max_count = count
                most_voted = agent
        return most_voted

    def isRound(self):
        return self.remainingTurns() > 1

    def isAccusing(self):
        return self.remainingTurns() == 1 and len(self.getAccusations()) == 0

    def isVoting(self):
        return self.remainingTurns() == 1 and len(self.getAccusations()) > 0

    def setPlayers(self, agents):
        if not isinstance(agents, (list, tuple)):
            raise TypeError("Players must be a list or tuple")

        if len(agents) > self.getBoardSize() ** 2:
            raise ValueError("Number of agents must be less than or equal to the board size squared.")

        self.agents = agents

        if not all(isinstance(agent, Agent) for agent in agents):
            raise ValueError("Players must be a list or tuple of agents.")
        
        if len(agents) < 2:
            raise ValueError("There must be at least two agents.")
        
        if len(agents) == 0:
            for i in range(agents):
                self.agents.append(RandomWalker(self, 0, lambda x: 0))

        for agent in self.agents:
            position = tuple(floor(random() * self.getBoardSize()) for i in range(2))
            agent.setPosition(position)
            self.getBoard().addAgent(position[0], position[1], agent)

    def setNumRounds(self, num_rounds):
        if not isinstance(num_rounds, int) or num_rounds < 0:
            raise ValueError("Number of rounds must be a positive integer.")
        self.num_rounds = num_rounds

    def setNumTurns(self, num_turns):
        if not isinstance(num_turns, int) or num_turns < 0:
            raise ValueError("Number of turns must be a positive integer.")
        self.num_turns = num_turns

    def setCurrentRound(self, current_round):
        if not isinstance(current_round, int) or current_round < 0:
            raise ValueError("Current round must be a positive integer.")
        if current_round >= self.getNumRounds():
            raise ValueError("Current round must be less than the number of rounds.")
        self.current_round = current_round

    def setCurrentTurn(self, current_turn):
        if not isinstance(current_turn, int) or current_turn < 0:
            raise ValueError("Current turn must be a positive integer.")
        if current_turn >= self.getNumTurns():
            raise ValueError("Current turn must be less than the number of turns.")
        self.current_turn = current_turn

    def setDone(self, done):
        if not isinstance(done, bool):
            raise ValueError("Done must be a boolean")
        self.done = done

    def setAccusations(self, accusations):
        self.accusations = accusations

    def setVotes(self, votes):
        self.votes = votes

    def setImprisoned(self, imprisoned):
        self.imprisoned = imprisoned

    def remainingTurns(self):
        return self.getNumTurns() - self.getCurrentTurn()
    
    def remainingRounds(self):
        return self.getNumRounds() - self.getCurrentRound()
    
    def nextRound(self):
        self.setCurrentRound(self.getCurrentRound() + 1)
        self.setCurrentTurn(0)
        self.board.growResources(self.getResourceGrowthFrequency())

        # Reset agents' round endowments
        for agent in self.getAgents():
            agent.setRoundEndowment(0)

    def nextTurn(self):
        self.setCurrentTurn(self.getCurrentTurn() + 1)

    def step(self):
        if self.getDone():
            return
        
        if self.isAccusing():
            # Collect accusations from agents
            accusations = {}
            for agent in self.getAgents():
                accusations[agent] = agent.accuse()
            self.setAccusations(accusations)
        elif self.isVoting():
            accused = self.getMostAccused()
            self.setAccusations({})

            # Release the last accused agent
            self.setImprisoned(None)

            if accused is not None:
                # Share information about the accused agent's consumption
                consumption = set()
                for agent in self.getAgents():
                    consumption = consumption | agent.getSeenGathers(accused)

                # Collect votes from agents
                votes = {}
                no_votes = 0
                yes_votes = 0
                for agent in self.getAgents():
                    votes[agent] = agent.vote(consumption, accused)
                    if votes[agent]:
                        yes_votes += 1
                    else:
                        no_votes += 1
                self.setVotes(votes)

                print(f"YES: {yes_votes}, NO: {no_votes} (accused: {accused.getId()})")
                if yes_votes > no_votes:
                    # Imprison the accused agent
                    print(f"{accused.getId()} was imprisoned.")
                    self.setImprisoned(accused)

            if self.remainingRounds() == 1:
                self.setDone(True)
            else:
                self.nextRound()
        else: # Normal turn
            # Advance the timestamp of the board cells
            timestamp = self.getCurrentTurn() + self.getCurrentRound() * self.getNumTurns()
            self.getBoard().setTimestamp(timestamp)

            # Collect actions from agents
            new_actions = []
            for agent in self.getAgents():
                if self.getImprisoned() != agent: # Skip imprisoned agent
                    seen_actions = [(ag, ac) for ag, ac in self.actions if ag != agent and agent.canSee(ag.getPosition()[0], ag.getPosition()[1])]
                    new_actions.append((agent, agent.act(timestamp, self.getBoard(), seen_actions)))
            self.actions = new_actions

            # Execute actions in a random order
            self.actions.sort(key=lambda x: random())
            for agent, action in self.actions:
                action.execute(agent, self.getBoard())

            if self.remainingTurns() == 1:
                if self.remainingRounds() == 1:
                    self.setDone(True)
            else:
                self.nextTurn()


    def __str__(self):
        return "Game: " + str(self.__class__) + "\n" + \
                "Board: " + str(self.board) + "\n" + \
                "Players: " + str(self.agents) + "\n" + \
                "Number of Players: " + str(len(self.agents)) + "\n" + \
                "Number of Rounds: " + str(self.num_rounds) + "\n" + \
                "Number of Turns: " + str(self.num_turns) + "\n"
