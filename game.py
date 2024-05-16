from random_walker import RandomWalker
from agents import Agent
from board import Board

from math import floor
from random import random

class Game:
    def __init__(self, board=None, players=[], num_rounds=1, num_turns=1):
        self.setBoard(board)
        self.setNumRounds(num_rounds)
        self.setNumTurns(num_turns)
        self.setPlayers(players)
        self.setCurrentRound(0)
        self.setCurrentTurn(0)
        self.setDone(False)
        self.setTotalReward(0)
        self.setAccusations({})
        self.setVotes({})
        self.setImprisoned(None)

    def getBoard(self):
        return self.board
    
    def getPlayers(self):
        return self.players
    
    def getBoardSize(self):
        return self.board.getBoardSize()
    
    def getNumRounds(self):
        return self.num_rounds
    
    def getNumTurns(self):
        return self.num_turns
    
    def getCurrentRound(self):
        return self.current_round
    
    def getCurrentTurn(self):
        return self.current_turn

    def getTotalReward(self):
        return self.total_reward

    def getAccusations(self):
        return self.accusations

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

    def getVotes(self):
        return self.votes
    
    def getMostVoted(self):
        max_count = 0
        most_voted = None
        for player, count in self.getVotes().items():
            if count > max_count:
                max_count = count
                most_voted = player
        return most_voted

    def getDone(self):
        return self.done

    def getImprisoned(self):
        return self.imprisoned

    def isRound(self):
        return self.remainingTurns() > 1

    def isAccusing(self):
        return self.remainingTurns() == 1 and len(self.getAccusations()) == 0

    def isVoting(self):
        return self.remainingTurns() == 1 and len(self.getAccusations()) > 0
    
    def setBoard(self, board):
        if not isinstance(board, Board):
            raise TypeError("Board must be of type Board")
        self.board = board

    def setPlayers(self, players):
        if not isinstance(players, (list, tuple)):
            raise TypeError("Players must be a list or tuple")

        if len(players) > self.getBoardSize() ** 2:
            raise ValueError("Number of players must be less than or equal to the board size squared.")

        self.players = players

        if not all(isinstance(player, Agent) for player in players):
            raise ValueError("Players must be a list or tuple of agents.")
        
        if len(players) < 2:
            raise ValueError("There must be at least two players.")
        
        if len(players) == 0:
            for i in range(players):
                self.players.append(RandomWalker(self, 0, lambda x: 0))

        for player in self.players:
            position = tuple(floor(random() * self.getBoardSize()) for i in range(2))
            player.setPosition(position)
            self.getBoard().addAgent(position[0], position[1], player)

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

    def setTotalReward(self, total_reward):
        self.total_reward = total_reward

    def addTotalReward(self, reward):
        self.setTotalReward(self.getTotalReward() + reward)

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
        self.board.growResources()

        # TODO - vote

    def nextTurn(self):
        self.setCurrentTurn(self.getCurrentTurn() + 1)

    def step(self):
        if self.getDone():
            return
        
        if self.isAccusing():
            # Collect accusations from players
            accusations = {}
            for player in self.getPlayers():
                accusations[player] = player.accuse()
            self.setAccusations(accusations)
        elif self.isVoting():
            accused = self.getMostAccused()
            self.setAccusations({})

            # Release the last accused player
            if self.getImprisoned() is not None:
                self.getBoard().addAgent(self.getImprisoned().getPosition()[0], self.getImprisoned().getPosition()[1], self.getImprisoned())
                self.setImprisoned(None)

            # Share information about the accused player's consumption
            consumption = {}
            for player in self.getPlayers():
                consumption = consumption | player.disclose_consumption(accused)

            # Collect votes from players
            votes = {}
            no_votes = 0
            yes_votes = 0
            for player in self.getPlayers():
                votes[player] = player.vote(consumption, accused)
                if votes[player]:
                    yes_votes += 1
                else:
                    no_votes += 1
            self.setVotes(votes)

            print(f"YES: {yes_votes}, NO: {no_votes} (accused: {accused.getId()})")
            if yes_votes > no_votes:
                # Imprison the accused player
                print(f"{accused.getId()} was imprisoned.")
                self.setImprisoned(accused)

            if self.remainingRounds() == 1:
                self.setDone(True)
            else:
                self.nextRound()
        else: # Normal turn
            # print(f"Round {self.getCurrentRound()}, Turn {self.getCurrentTurn()}")
            # print("aaaaaa")
            for player in self.getPlayers():
                if self.getImprisoned() != player: # Skip imprisoned player
                    # print("bbbbbb")
                    self.addTotalReward(player.act())
            # exit(0)

            if self.remainingTurns() == 1:
                if self.remainingRounds() == 1:
                    self.setDone(True)
            else:
                self.nextTurn()


    def __str__(self):
        return "Game: " + str(self.__class__) + "\n" + \
                "Board: " + str(self.board) + "\n" + \
                "Players: " + str(self.players) + "\n" + \
                "Number of Players: " + str(len(self.players)) + "\n" + \
                "Number of Rounds: " + str(self.num_rounds) + "\n" + \
                "Number of Turns: " + str(self.num_turns) + "\n"
