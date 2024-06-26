from .agent import Agent
from .board import Board

from math import floor
from random import random

from statistics import *

class Game:

    class GameStats:
        def __init__(self, game):
            self.game = game
            self.round_stats = []
            self.average_endowment = []
            self.median_endowment = []
            self.max_endowment = []
            self.min_endowment = []
            self.variance_endowment = []
            self.standard_deviation_endowment = []
            self.stats_round = 0
            self.total_rewards = []

        def computeRoundStats(self):
            round_stats = {}
            round_stats["average_endowment"] = self.getAverageEndowmentByBehavior()
            round_stats["median_endowment"] = self.getMedianEndowmentByBehavior()
            round_stats["max_endowment"] = self.getMaxEndowmentByBehavior()
            round_stats["min_endowment"] = self.getMinEndowmentByBehavior()
            round_stats["variance_endowment"] = self.getVarianceEndowmentByBehavior()
            round_stats["standard_deviation_endowment"] = self.getStandardDeviationEndowmentByBehavior()
            round_stats["total_reward"] = self.game.getTotalReward()
            self.stats_round = self.game.getCurrentRound()
            return round_stats

        def append(self, round_stats):
            self.round_stats.append(round_stats)
            self.average_endowment.append(round_stats["average_endowment"])
            self.median_endowment.append(round_stats["median_endowment"])
            self.max_endowment.append(round_stats["max_endowment"])
            self.min_endowment.append(round_stats["min_endowment"])
            self.variance_endowment.append(round_stats["variance_endowment"])
            self.standard_deviation_endowment.append(round_stats["standard_deviation_endowment"])
            self.total_rewards.append(round_stats["total_reward"])

        def getTotalRewardsPerRound(self):
            return self.total_rewards
        
        def getEndowmentsByBehavior(self):
            endowments = {}
            for agent in self.game.agents: # for each agent
                behavior = agent.getBehavior() # get the behavior
                behavior_str = behavior.__str__()
                if behavior_str not in endowments: # if the behavior is not in the endowments
                    endowments[behavior_str] = [] # create a list for the behavior
                endowments[behavior_str].append(agent.roundEndowment) # append the agent's endowment to the behavior's list
            return endowments

        def getAverageEndowmentByBehavior(self):
            endowments = self.getEndowmentsByBehavior()

            # average it by number of players
            num_players = self.game.getNumOfAgentTypes()
            for behavior, endowment in endowments.items(): # for each behavior and its endowment list
                endowments[behavior] = sum(endowment) / num_players[behavior] # average the endowment list by the number of players

            return endowments # return the endowments
        
        def getMedianEndowmentByBehavior(self):
            endowments = self.getEndowmentsByBehavior()
            
            for behavior, endowment in endowments.items(): # for each behavior and its endowment list
                endowments[behavior] = median(endowment) # get the median of the endowment list

            return endowments # return the endowments

        def getMaxEndowmentByBehavior(self):
            endowments = self.getEndowmentsByBehavior()

            for behavior, endowment in endowments.items():
                endowments[behavior] = max(endowment)
            
            return endowments # return the endowments

        def getMinEndowmentByBehavior(self):
            endowments = self.getEndowmentsByBehavior()

            for behavior, endowment in endowments.items(): # for each behavior and its endowment list
                endowments[behavior] = min(endowment) # get the minimum of the endowment list
            
            return endowments # return the endowments
        
        def getVarianceEndowmentByBehavior(self):
            endowments = self.getEndowmentsByBehavior()

            num_players = self.game.getNumOfAgentTypes()
            for behavior, endowment in endowments.items():

                mean = sum(endowment) / num_players[behavior]
                endowments[behavior] = sum((x - mean) ** 2 for x in endowment) / num_players[behavior]

            return endowments
        
        def getStandardDeviationEndowmentByBehavior(self):
            endowments = self.getEndowmentsByBehavior()

            num_players = self.game.getNumOfAgentTypes()   
            for behavior, endowment in endowments.items():
                    
                mean = sum(endowment) / num_players[behavior]
                endowments[behavior] = (sum((x - mean) ** 2 for x in endowment) / num_players[behavior]) ** 0.5

            return endowments

        def getStats(self):
            return self.round_stats
        
        def getStatsType(self, stats_type):
            if stats_type == "average_endowment":
                return self.average_endowment
            elif stats_type == "median_endowment":
                return self.median_endowment
            elif stats_type == "max_endowment":
                return self.max_endowment
            elif stats_type == "min_endowment":
                return self.min_endowment
            elif stats_type == "variance_endowment":
                return self.variance_endowment
            elif stats_type == "standard_deviation_endowment":
                return self.standard_deviation_endowment
        
        def getStatsRound(self):
            return self.stats_round
        
        def sortStatsInList(self, stats_type):
            stats_list = []
            stats = self.getStatsType(stats_type)
            for i in range(len(stats)):
                for val in stats[i].values():
                    stats_list.append(val)
            return stats_list
        
        def fillTypeStats(self, key):
            filler_value = 0
            num_rounds = self.game.getNumRounds()
            fill_count = num_rounds - len(self.sortStatsInList(key))
            extended = self.sortStatsInList(key) + [filler_value] * fill_count
            return extended
        
        def fillCumulative(self):
            filler_value = self.getTotalRewardsPerRound()[-1]
            num_rounds = self.game.getNumRounds()
            fill_count = num_rounds - len(self.getTotalRewardsPerRound())
            extended = self.getTotalRewardsPerRound() + [filler_value] * fill_count
            return extended
            
        def printStats(self):
            print("Round: ", self.stats_round + 1)
            print("Average endowment: ", self.average_endowment)
            print("Median endowment: ", self.median_endowment)
            print("Max endowment: ", self.max_endowment)
            print("Min endowment: ", self.min_endowment)
            print("Variance endowment: ", self.variance_endowment)
            print("Standard deviation endowment: ", self.standard_deviation_endowment)
            print("Total rewards: ", self.total_rewards)
            print("")


    ###########################
    ###     Constructor     ###
    ###########################

    def __init__(self, board_size, behaviors, sight_radius, resource_frequency, resource_growth_frequency, num_rounds, num_turns):
        self.board = Board(board_size)
        self.agents = []
        self.num_rounds = num_rounds
        self.num_turns = num_turns
        self.resource_growth_frequency = resource_growth_frequency
        self.stats = Game.GameStats(self)

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
        self.number_of_votes = (0, 0)
        self.accused = None
        self.previous_positions = { agent: agent.getPosition() for agent in self.getAgents() }
        self.num_banned_agents = { agent: 0 for agent in self.getNumOfAgentTypes()}

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
    
    def getNumberOfVotes(self):
        return self.number_of_votes

    def getDone(self):
        return self.done

    def getMostAccused(self):
        return self.accused

    def getResourceGrowthFrequency(self):
        return self.resource_growth_frequency
    
    def getNumBannedAgentsByBehavior(self):
        return self.num_banned_agents

    ###########################
    ###       Methods       ###
    ###########################
    
    def getNumOfAgentTypes(self):
        agent_types = {}
        for agent in self.getAgents():
            behavior_str = agent.getBehavior().__str__() 
            if behavior_str not in agent_types:
                agent_types[behavior_str] = 0
            agent_types[behavior_str] += 1
        return agent_types

    def getTotalReward(self):
        return sum(agent.getEndowment() for agent in self.getAgents())
    
    def getTotalRewardByBehavior(self):
        rewards = {}
        for agent in self.getAgents():
            behavior = agent.getBehavior()
            behavior_str = behavior.__str__()
            if behavior_str not in rewards:
                rewards[behavior_str] = 0
            rewards[behavior_str] += agent.getEndowment()
        return rewards
    
    def getOrderedAccusedList(self):
        accusation_count = {}
        for player in self.getAgents():
            if not player.isImprisoned():
                accusation_count[player] = 0
        for accused in self.getAccusations().values():
            if accused in accusation_count:
                accusation_count[accused] += 1
        return {k: v for k, v in sorted(accusation_count.items(), key=lambda item: item[1], reverse=True)}
    
    def getMostVoted(self):
        max_count = 0
        most_voted = None
        for agent, count in self.getVotes().items():
            if count > max_count:
                max_count = count
                most_voted = agent
        return most_voted
    
    def setNumberOfVotes(self, yes, no):
        self.number_of_votes = (yes, no)

    def isRound(self):
        return self.remainingTurns() > 1

    def isAccusing(self):
        return self.remainingTurns() == 1 and len(self.getAccusations()) == 0

    def isVoting(self):
        return self.remainingTurns() == 1 and len(self.getAccusations()) > 0

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
    
    def addBannedAgents(self, agent):
        behavior = agent.getBehavior().__str__()
        print(f"{behavior} was banned.")
        if behavior not in self.num_banned_agents:
            self.num_banned_agents[behavior] = 0
        self.num_banned_agents[behavior] += 1

    def imprison(self, agent):
        agent.imprison()
        self.addBannedAgents(agent)
        self.getBoard().takeAgent(*agent.getPosition())

    def remainingTurns(self):
        return self.getNumTurns() - self.getCurrentTurn()
    
    def remainingRounds(self):
        return self.getNumRounds() - self.getCurrentRound()
    
    def nextRound(self):
        self.setCurrentRound(self.getCurrentRound() + 1)
        self.setCurrentTurn(0)

        # Grow resources on both the board and the agents' views
        self.board.growResources(self.getResourceGrowthFrequency())
        for agent in self.getAgents():
            # Won't necessarily match the real resource growth, but it's a good approximation.
            agent.getView().growResources(self.getResourceGrowthFrequency())

        # Reset agents' round endowments
        for agent in self.getAgents():
            agent.setRoundEndowment(0)

    def nextTurn(self):
        self.setCurrentTurn(self.getCurrentTurn() + 1)

    def step(self):
        if self.getDone():
            return self.stats
        
        if self.isAccusing():
            # Collect accusations from agents
            accusations = {}
            for agent in self.getAgents():
                if not agent.isImprisoned():
                    accusations[agent] = agent.accuse()
            self.setAccusations(accusations)
            
        elif self.isVoting():
            self.accused = list(self.getOrderedAccusedList().keys())[0]
            self.setAccusations({})
            
            if self.accused is not None:
                # Share information about the accused agent's consumption
                consumption = set()
                for agent in self.getAgents():
                    consumption = consumption | agent.getSeenGathers(self.accused)

                # Collect votes from agents
                votes = {}
                no_votes = 0
                yes_votes = 0
                for agent in self.getAgents():
                    if not agent.isImprisoned():
                        votes[agent] = agent.vote(consumption, self.accused)
                        if votes[agent]:
                            yes_votes += 1
                        else:
                            no_votes += 1
                self.setVotes(votes)

                print(f"YES: {yes_votes}, NO: {no_votes} (accused: {self.accused.getId()})")
                self.setNumberOfVotes(yes_votes, no_votes)
                if yes_votes > no_votes:
                    # Imprison the accused agent
                    print(f"{self.accused.getId()} was imprisoned.")
                    self.imprison(self.accused)
             
            # Compute statistics
            stats = self.stats.computeRoundStats()
            self.stats.append(stats)               
            if self.remainingRounds() == 1 or self.getBoard().getNumberOfResources() == 0:
                self.setDone(True)
            else:
                self.nextRound()
        else: # Normal turn
            #Verify if the game is over
            if self.getBoard().getNumberOfResources() == 0:
                stats = self.stats.computeRoundStats()
                self.stats.append(stats)
                self.setDone(True)
                return self.stats
                    
            # Advance the timestamp of the board cells
            timestamp = self.getCurrentTurn() + self.getCurrentRound() * self.getNumTurns() + 1
            self.getBoard().setTimestamp(timestamp)

            # Make agents communicate
            for ag1 in self.getAgents():
                for ag2 in self.getAgents():
                    if ag1 != ag2 and ag1.canSee(*ag2.getPosition()):
                        ag1.receiveInformation(ag2)

            # Collect actions from agents
            new_actions = []
            for agent in self.getAgents():
                if not agent.isImprisoned(): # Skip imprisoned agents
                    seen_actions = [(ag, ac) for ag, ac in self.actions if ag != agent and agent.couldSee(*self.previous_positions[agent], *self.previous_positions[ag])]
                    new_actions.append((agent, agent.act(self.getBoard(), seen_actions)))
            self.actions = new_actions

            # Execute actions in a random order
            self.actions.sort(key=lambda x: random())
            for agent, action in self.actions:
                self.previous_positions[agent] = agent.getPosition()
                action.execute(agent, self.getBoard())

            self.nextTurn()
        
        return self.stats


    def __str__(self):
        return "Game: " + str(self.__class__) + "\n" + \
                "Board: " + str(self.board) + "\n" + \
                "Players: " + str(self.agents) + "\n" + \
                "Number of Players: " + str(len(self.agents)) + "\n" + \
                "Number of Rounds: " + str(self.num_rounds) + "\n" + \
                "Number of Turns: " + str(self.num_turns) + "\n"
