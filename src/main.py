from behavior import RandomBehavior, GreedyBehavior, CooperativeBehavior
from environment import Game
from ui import CellSprite, UI

import pygame


if __name__ == "__main__":
    # Set some parameters
    cell_size = 32
    sprite_scale = cell_size / 16
    board_size = 32
    resource_frequency = 0.1
    resource_growth_frequency = 0.2
    sight_radius = 4
    num_rounds = 100
    num_turns = 50 # Turns per round
    turn_time = 25 # Milliseconds per game turn
    accusation_individual_time = 2000 # Milliseconds the accusation screen is shown
    accusation_ranking_time = 2000 # Milliseconds the accusation results screen is shown
    voting_individual_time = 2000 # Milliseconds the voting screen is shown
    voting_result_time = 2000 # Milliseconds the voting results screen is shown

    agent_count = 50

    # Initialize behaviors and environment
    # behaviors = [RandomBehavior(resource_growth_frequency) for i in range(agent_count)]
    # behaviors = [CooperativeBehavior(resource_growth_frequency) for i in range(agent_count)]
    behaviors = [GreedyBehavior(resource_growth_frequency) for i in range(agent_count)]
    game = Game(board_size, behaviors, sight_radius, resource_frequency, resource_growth_frequency, num_rounds, num_turns)

    # Setup pygame
    pygame.init()
    screen = pygame.display.set_mode([board_size * cell_size, board_size * cell_size])
    ui = UI(game, screen, cell_size, sprite_scale)

    # Prepare agent sprites
    ui.setAgentSprites()

    # Prepare variables to store statistics
    stats = {"average_endowment": [], "median_endowment": [], 
             "max_endowment": [], "min_endowment": [], 
             "variance_endowment": [], "standard_deviation_endowment": []}
    

    running = True
    last_step_time = pygame.time.get_ticks()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time = pygame.time.get_ticks()
        if game.isRound():
            if game.getCurrentRound() > 0 and game.getCurrentTurn() == 0 and current_time < last_step_time + voting_individual_time:
                ui.drawPopUpVotingList()
            elif game.getCurrentRound() > 0 and game.getCurrentTurn() == 0 and current_time < last_step_time + voting_individual_time + voting_result_time:
                ui.drawPopUpVotingResult()
            else:
                # If enough time has passed, advance a turn
                if current_time >= last_step_time + turn_time:
                    last_step_time = current_time
                    round_stats = game.step()

                    # Store statistics
                    stats["average_endowment"].append(round_stats.average_endowment)
                    stats["median_endowment"].append(round_stats.median_endowment)
                    stats["max_endowment"].append(round_stats.max_endowment)
                    stats["min_endowment"].append(round_stats.min_endowment)
                    stats["variance_endowment"].append(round_stats.variance_endowment)
                    stats["standard_deviation_endowment"].append(round_stats.standard_deviation_endowment)

                    print("Round: ", game.getCurrentRound(), " Turn: ", game.getCurrentTurn())
                    print("Average endowment: ", round_stats.average_endowment)
                    print("Median endowment: ", round_stats.median_endowment)
                    print("Max endowment: ", round_stats.max_endowment)
                    print("Min endowment: ", round_stats.min_endowment)
                    print("Variance endowment: ", round_stats.variance_endowment)
                    print("Standard deviation endowment: ", round_stats.standard_deviation_endowment)
                    print("")

                # Draw the board
                ui.drawBoard()
                
        elif game.isAccusing():
            game.step()
        elif game.isVoting():
            if current_time < last_step_time + accusation_individual_time:
                ui.drawPopUpAccusationList()
            elif current_time < last_step_time + accusation_individual_time + accusation_ranking_time:
                ui.drawPopUpAccusationRanking()
            else:
                last_step_time = current_time
                game.step()

        pygame.display.flip()

    pygame.quit()