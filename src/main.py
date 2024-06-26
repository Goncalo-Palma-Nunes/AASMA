from behavior import RandomBehavior, GreedyBehavior, CooperativeBehavior, AdversarialBehavior
from environment import Game
from ui import UI
from analysis import Analyse_Data, Individual_Plot

import pygame

if __name__ == "__main__":
    # Set some parameters
    speed_multiplier = 20
    cell_size = 32
    sprite_scale = cell_size / 16
    board_size = 32
    resource_frequency = 0.1
    resource_growth_frequency = 0.2
    sight_radius = 4
    num_rounds = 20
    num_turns = 100 # Turns per round
    turn_time = 200 / speed_multiplier # Milliseconds per game turn
    accusation_individual_time = 1000 / speed_multiplier # Milliseconds the accusation screen is shown
    accusation_ranking_time = 2000 / speed_multiplier # Milliseconds the accusation results screen is shown
    voting_individual_time = 1000 / speed_multiplier # Milliseconds the voting screen is shown
    voting_result_time = 2000 / speed_multiplier # Milliseconds the voting results screen is shown

    random_count = 0
    greedy_count = 0
    cooperative_count = 0
    adversarial_count = 20

    # Initialize behaviors
    behaviors = []
    for i in range(random_count):
        behaviors.append(RandomBehavior())
    for i in range(greedy_count):
        behaviors.append(GreedyBehavior())
    for i in range(cooperative_count):
        behaviors.append(CooperativeBehavior(resource_frequency, resource_growth_frequency))
    for i in range(adversarial_count):
        behaviors.append(AdversarialBehavior(resource_frequency, resource_growth_frequency))
    agent_count = len(behaviors)

    # Initialize the game
    game = Game(board_size, behaviors, sight_radius, resource_frequency, resource_growth_frequency, num_rounds, num_turns)

    # Setup pygame
    pygame.init()
    screen = pygame.display.set_mode([board_size * cell_size, board_size * cell_size])
    ui = UI(game, screen, cell_size, sprite_scale)

    # Prepare agent sprites
    ui.setAgentSprites()

    running = True
    done = False
    last_step_time = pygame.time.get_ticks()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time = pygame.time.get_ticks()
        
        if game.getDone():
            if not done:
                round_stats.printStats()
                print(game.getTotalRewardByBehavior(), game.getNumBannedAgentsByBehavior())
                analyse = Analyse_Data()
                analyse.receiveData(game.getTotalRewardByBehavior(), 'total_rewards')
                analyse.receiveData(round_stats.fillCumulative(), 'cumulative_rewards')
                plot = Individual_Plot(game, round_stats)
                keys = list(round_stats.getStats()[0].keys())[:-1]
                for key in keys:
                    plot.callStatsTypePlots(key)
                    analyse.receiveData(round_stats.fillTypeStats(key), f'{key}_per_round')
                plot.callBarTypePlots()
                done = True 
            ui.drawBoard()
            ui.drawGameOver()
            
        elif game.isRound():
            if game.getCurrentRound() > 0 and game.getCurrentTurn() == 0 and current_time < last_step_time + voting_individual_time:
                ui.drawPopUpVotingList()
            elif game.getCurrentRound() > 0 and game.getCurrentTurn() == 0 and current_time < last_step_time + voting_individual_time + voting_result_time:
                ui.drawPopUpVotingResult()
            else:
                # If enough time has passed, advance a turn
                if current_time >= last_step_time + turn_time:
                    last_step_time = current_time
                    round_stats = game.step()

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
                round_stats = game.step()
                round_stats.printStats()

        pygame.display.flip()

    pygame.quit()