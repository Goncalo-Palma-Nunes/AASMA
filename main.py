from board import Board
from random_walker import RandomWalker
from game import Game

import pygame

class CellSprite:
    def __init__(self, cell_size, image, offset=(0,0)):
        self.cell_size = cell_size
        self.image = image
        self.offset = offset

    @staticmethod
    def fromFile(cell_size, scale, path):
        src_image = pygame.image.load(path)
        src_image = pygame.transform.scale_by(src_image, (scale, scale))

        image = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA, 32)
        image_center = (cell_size / 2, cell_size / 2)
        image.blit(src_image, src_image.get_rect(center=image_center))

        return CellSprite(cell_size, image)

    def getImage(self):
        return self.image

    def drawTo(self, surface, i, j):
        surface.blit(self.image, (i * self.cell_size + self.offset[0], j * self.cell_size + self.offset[1]))

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

    # Initialize board and game
    board = Board(board_size, resource_frequency, resource_growth_frequency)
    board.generateResources()
    players = [RandomWalker(board, 0, lambda x: 0) for i in range(player_count)]
    game = Game(board, players, num_rounds, num_turns)

    # Setup pygame
    pygame.init()
    screen = pygame.display.set_mode([board.getBoardSize() * cell_size, board.getBoardSize() * cell_size])

    # Load sprites
    apple_sprite = CellSprite.fromFile(cell_size, 2, "assets/apple.png")
    grass_sprite = CellSprite.fromFile(cell_size, 2, "assets/grass.png")
    slime_sprites = ["slime_bluegreen.png", "slime_gold.png", "slime_pink.png", "slime_purple.png"]
    slime_sprites = [CellSprite.fromFile(cell_size, 2, f"assets/{name}") for name in slime_sprites]

    # Prepare agent sprites
    font = pygame.font.SysFont(None, 20)
    agent_sprites = {}
    for player in game.getPlayers():
        id_text = font.render(str(player.getId()), True, (0, 0, 0))
    
        image_size = (max(cell_size, id_text.get_rect().width), cell_size + id_text.get_rect().height)
        image_offset = (min(0, cell_size - id_text.get_rect().width) / 2, -id_text.get_rect().height)

        image = pygame.Surface(image_size, pygame.SRCALPHA, 32)
        image.blit(slime_sprites[0].getImage(), (-image_offset[0], -image_offset[1]))
        image.blit(id_text, ((image_size[0] - id_text.get_rect().width) / 2, 0))

        agent_sprites[player.getId()] = CellSprite(cell_size, image, offset=(0, image_offset[1]))

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

                if not cell.noResource():
                    apple_sprite.drawTo(screen, i, j)
                if not cell.noAgent():
                    agent_sprites[cell.getAgent().getId()].drawTo(screen, i, j)

        pygame.display.flip()

    pygame.quit()