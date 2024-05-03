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

    def getDone(self):
        return self.done
    
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

        for player in self.getPlayers():
            self.addTotalReward(player.act())

        if self.remainingTurns() == 1:
            if self.remainingRounds() == 1:
                self.setDone(True)
            else:
                self.nextRound()
        else:
            self.nextTurn()

    def __str__(self):
        return "Game: " + str(self.__class__) + "\n" + \
                "Board: " + str(self.board) + "\n" + \
                "Players: " + str(self.players) + "\n" + \
                "Number of Players: " + str(len(self.players)) + "\n" + \
                "Number of Rounds: " + str(self.num_rounds) + "\n" + \
                "Number of Turns: " + str(self.num_turns) + "\n"
