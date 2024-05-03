from board import Board
from random_walker import RandomWalker
from game import Game

import pygame

if __name__ == "__main__":
    cell_size = 32
    board_size = 32
    resource_frequency = 0.1
    resource_growth_frequency = 0.2
    num_rounds = 100
    num_turns = 50 # Turns per round
    step_time = 10 # Milliseconds per game step
    player_count = 20

    # Initialize board and game
    board = Board(board_size, resource_frequency, resource_growth_frequency)
    board.generateResources()
    players = [RandomWalker(board, 0, lambda x: 0) for i in range(player_count)]
    game = Game(board, players, num_rounds, num_turns)

    pygame.init()
    screen = pygame.display.set_mode([board.getBoardSize() * cell_size, board.getBoardSize() * cell_size])
    running = True

    last_step_time = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # If enough time has passed, step the game
        current_time = pygame.time.get_ticks()
        if current_time >= last_step_time + step_time:
            last_step_time = current_time
            game.step()
            
        # Draw the board
        screen.fill((0, 200, 0))
        for i in range(board.getBoardSize()):
            for j in range(board.getBoardSize()):
                cell_center = ((i + 0.5) * cell_size, (j + 0.5) * cell_size)

                cell = board.getCell(i, j)
                if cell.noAgent():
                    if cell.noResource():
                        # TODO: draw grass sprite
                        pass
                    else:
                        # TODO: draw resource sprite
                        pygame.draw.circle(screen, (200, 0, 0), cell_center, 0.25 * cell_size)
                else:
                    # TODO: draw agent sprite
                    pygame.draw.circle(screen, (0, 0, 200), cell_center, 0.4 * cell_size)
        pygame.display.flip()

    pygame.quit()