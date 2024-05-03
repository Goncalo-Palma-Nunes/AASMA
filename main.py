from board import Board
from random_walker import RandomWalker
from game import Game

import pygame

if __name__ == "__main__":
    cell_size = 32
    board = Board(32)
    board.generateResources()
    players = [RandomWalker(board, 0, lambda x: 0) for i in range(2)]
    game = Game(board, players, num_rounds=1, num_turns=1)

    pygame.init()
    screen = pygame.display.set_mode([board.getBoardSize() * cell_size, board.getBoardSize() * cell_size])
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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