from random_walker import RandomWalker
from agents import Agent
from board import Board

class Game:
    def __init__(self, board=None, players=[], num_players=2,
                num_rounds=1, num_turns=1):
        self.setNumPlayers(num_players)
        self.setNumRounds(num_rounds)
        self.setNumTurns(num_turns)
        self.setBoard(board)
        self.setPlayers(players)
        self.setCurrentRound(0)
        self.setCurrentTurn(0)

    def getBoard(self):
        return self.board
    
    def getPlayers(self):
        return self.players
    
    def getBoardSize(self):
        return self.board.getBoardSize()
    
    def getNumPlayers(self):
        return self.num_players
    
    def getNumRounds(self):
        return self.num_rounds
    
    def getNumTurns(self):
        return self.num_turns
    
    def getCurrentRound(self):
        return self.current_round
    
    def getCurrentTurn(self):
        return self.current_turn
    
    def setBoard(self, board):
        if not isinstance(board, Board):
            raise TypeError("Board must be of type Board")
        self.board = board

    def setPlayers(self, players):
        if not isinstance(players, (list, tuple)):
            raise TypeError("Players must be a list or tuple")
        self.players = players

        if len(players) != self.getNumPlayers():
            raise ValueError("Number of players must match the number of players in the game.")

        if not all(isinstance(player, Agent) for player in players):
            raise ValueError("Players must be a list or tuple of agents.")
        
        if len(players) < 2:
            raise ValueError("There must be at least two players.")
        
        if len(players) == 0:
            for i in range(players):
                self.players.append(RandomWalker(self, 0, lambda x: 0))

    def setNumPlayers(self, num_players):
        if not isinstance(num_players, int) or num_players < 0:
            raise ValueError("Number of players must be a positive integer.")
        if num_players > self.getBoard().getBoardSize():
            raise ValueError("Number of players must be less than the board size.")
        self.num_players = num_players

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

    def play(self):
        total_reward = 0

        for i in range(self.getNumRounds()):
            for j in range(self.getNumTurns()):
                for player in self.getPlayers():
                    total_reward += player.act()

                self.nextTurn()

            self.nextRound()

        return total_reward

    def __str__(self):
        return "Game: " + str(self.__class__) + "\n" + \
                "Board: " + str(self.board) + "\n" + \
                "Players: " + str(self.players) + "\n" + \
                "Number of Players: " + str(self.num_players) + "\n" + \
                "Number of Rounds: " + str(self.num_rounds) + "\n" + \
                "Number of Turns: " + str(self.num_turns) + "\n"
    

if __name__ == "__main__":
    board = Board(3)
    board.generateResources()
    board.printBoard()
    #players = [RandomWalker(board, 0, lambda x: 0) for i in range(2)]
    #game = Game(board, players, 2, 1, 1, 1.0)