from board import Board
from random_walker import RandomWalker
from game import Game
from ui import CellSprite, UI

import pygame

if __name__ == "__main__":
    # Set some parameters
    cell_size = 32
    sprite_scale = cell_size / 16
    board_size = 32
    resource_frequency = 0.1
    resource_growth_frequency = 0.2
    num_rounds = 2
    num_turns = 20 # Turns per round
    turn_time = 20 # Milliseconds per game turn
    accusation_individual_time = 2000 # Milliseconds the accusation screen is shown
    accusation_ranking_time = 2000 # Milliseconds the accusation results screen is shown
    voting_individual_time = 50 # Milliseconds the voting screen is shown
    voting_result_time = 50 # Milliseconds the voting results screen is shown

    player_count = 50

    # Initialize board and game
    board = Board(board_size, resource_frequency, resource_growth_frequency)
    players = [RandomWalker(board, 0, lambda x: 0) for i in range(player_count)]
    for i in range(player_count):
        players[i].setOtherPlayers(players[:i] + players[i+1:])

    board.generateResources()
    
    game = Game(board, players, num_rounds, num_turns)
    for i in range(player_count):
        players[i].setBoard(deep_copy=True) # Deep copy the board for each player

    # Setup pygame
    pygame.init()
    screen = pygame.display.set_mode([board.getBoardSize() * cell_size, board.getBoardSize() * cell_size])
    ui = UI(board, game, screen, cell_size, sprite_scale)

    # Prepare agent sprites
    ui.setAgentSprites()

    running = True
    last_step_time = pygame.time.get_ticks()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time = pygame.time.get_ticks()
        if game.isRound():
            if game.getCurrentRound() > 0 and game.getCurrentTurn() == 0 and current_time < last_step_time + voting_individual_time:
                # TODO: Show the votes of each agent
                pass
            elif game.getCurrentRound() > 0 and game.getCurrentTurn() == 0 and current_time < last_step_time + voting_individual_time + voting_result_time:
                # TODO: Show the final voting results
                pass
            else:
                # If enough time has passed, advance a turn
                if current_time >= last_step_time + turn_time:
                    last_step_time = current_time
                    game.step()
                # Draw the board
                ui.drawBoard()
                
        elif game.isAccusing():
            game.step()
        elif game.isVoting():
            if current_time < last_step_time + voting_individual_time:
                ui.drawPopUpAccusationList()
                    
            elif current_time < last_step_time + accusation_individual_time + accusation_ranking_time:
                pass # TODO: show accusation ranking popup.
            else:
                game.step()

        pygame.display.flip()

    pygame.quit()