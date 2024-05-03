from board import Board
from random_walker import RandomWalker
from game import Game

import pygame

class CellSprite:
    def __init__(self, cell_size, scale, path):
        self.cell_size = cell_size

        src_image = pygame.image.load(path)
        src_image = pygame.transform.scale_by(src_image, (scale, scale))

        self.image = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA, 32)
        image_center = (cell_size / 2, cell_size / 2)

        self.image.blit(src_image, src_image.get_rect(center=image_center))

    def drawTo(self, surface, i, j):
        surface.blit(self.image, (i * self.cell_size, j * self.cell_size))

if __name__ == "__main__":
    # Set some parameters
    cell_size = 32
    board_size = 32
    resource_frequency = 0.1
    resource_growth_frequency = 0.2
    num_rounds = 100
    num_turns = 50 # Turns per round
    step_time = 250 # Milliseconds per game step
    player_count = 20

    # Load sprites
    apple_sprite = CellSprite(cell_size, 2, "assets/apple.png")
    grass_sprite = CellSprite(cell_size, 2, "assets/grass.png")
    slime_sprites = ["slime_bluegreen.png", "slime_gold.png", "slime_pink.png", "slime_purple.png"]
    slime_sprites = [CellSprite(cell_size, 2, f"assets/{name}") for name in slime_sprites]

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
                grass_sprite.drawTo(screen, i, j)

                if cell.noAgent():
                    if not cell.noResource():
                        apple_sprite.drawTo(screen, i, j)
                else:
                    slime_sprites[0].drawTo(screen, i, j)
        pygame.display.flip()

    pygame.quit()