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
    
    def getWidth(self):
        return self.image.get_width()
    
    def getHeight(self):
        return self.image.get_height()

    def drawTo(self, surface, i, j):
        surface.blit(self.image, (i * self.cell_size + self.offset[0], j * self.cell_size + self.offset[1]))

if __name__ == "__main__":
    # Set some parameters
    cell_size = 32
    sprite_scale = cell_size / 16
    board_size = 32
    resource_frequency = 0.1
    resource_growth_frequency = 0.2
    num_rounds = 100
    num_turns = 25 # Turns per round
    turn_time = 250 # Milliseconds per game turn
    accusation_individual_time = 2000 # Milliseconds the accusation screen is shown
    accusation_ranking_time = 500 # Milliseconds the accusation results screen is shown
    voting_individual_time = 500 # Milliseconds the voting screen is shown
    voting_result_time = 500 # Milliseconds the voting results screen is shown

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

    # Load sprites
    apple_sprite = CellSprite.fromFile(cell_size, sprite_scale, "assets/apple.png")
    grass_sprite = CellSprite.fromFile(cell_size, sprite_scale, "assets/grass.png")
    jail_sprite = CellSprite.fromFile(cell_size, sprite_scale, "assets/jail.png")
    slime_sprites = ["slime_bluegreen.png", "slime_gold.png", "slime_pink.png", "slime_purple.png"]
    slime_sprites = [CellSprite.fromFile(cell_size, sprite_scale, f"assets/{name}") for name in slime_sprites]

    # Prepare agent sprites
    font = pygame.font.SysFont("arialblack", cell_size //2)
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
    step = 0
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
                    print("step", step)
                    step += 1
                    game.step()

                # Draw the board
                for i in range(board.getBoardSize()):
                    for j in range(board.getBoardSize()):
                        cell_center = ((i + 0.5) * cell_size, (j + 0.5) * cell_size)

                        cell = board.getCell(i, j)
                        grass_sprite.drawTo(screen, i, j)

                        if not cell.noResource():
                            apple_sprite.drawTo(screen, i, j)
                        if not cell.noAgent():
                            agent_sprites[cell.getAgent().getId()].drawTo(screen, i, j)
                            if cell.getAgent() == game.getImprisoned():
                                jail_sprite.drawTo(screen, i, j)
        elif game.isAccusing():
            game.step()
        elif game.isVoting():
            if current_time < last_step_time + accusation_individual_time:
                margin = 4
                row_size = 2
                col_size = 5

                new_font = pygame.font.SysFont("arialblack", cell_size)
                accusesText = font.render("accuses", True, (0, 0, 0))
                accusationText = new_font.render("Accusation List", True, (0,0,0))

                max_rows = board_size / row_size - margin

                cols = len(game.getPlayers()) // max_rows + 1
                rows = len(game.getPlayers()) // cols

                center = (board_size * cell_size / 2, board_size * cell_size / 2)
                box_size = (cols * col_size * cell_size, rows * row_size * cell_size)
                box_position = (center[0] - box_size[0] / 2, center[1] - box_size[1] / 2)
                
                box_size_background = (cols * col_size * cell_size + (row_size * cell_size /3), rows * row_size * cell_size + row_size * cell_size)
                box_position_background = (center[0] - box_size_background[0] / 2, center[1] - box_size_background[1] / 2 - (row_size * cell_size / 3))

                # Draw popup background
                pygame.draw.rect(screen, (161, 102, 47), (box_position_background, box_size_background))
                pygame.draw.rect(screen, (216, 181, 137), (box_position, box_size))
                
                
                screen.blit(accusationText, (box_position[0], box_position_background[1] + row_size * cell_size/ 6))

                for player, accused in game.getAccusations().items():
                    i = player.getId() // rows
                    j = player.getId() % rows
                    position = ((box_position[0] + i * col_size * cell_size) / cell_size, (box_position[1] + j * row_size * cell_size) / cell_size + 1)
                    
                    # Draw accusation boxes
                    accusation_box_size = (col_size * cell_size, row_size * cell_size)
                    accusation_box_position = (box_position[0] + i * col_size * cell_size, box_position[1] + j * row_size * cell_size)
                    pygame.draw.rect(screen, (161, 102, 47), (accusation_box_position, accusation_box_size), 1)
                    
                    # Draw player and accused sprites
                    agent_sprites[player.getId()].drawTo(screen, position[0], position[1])
                    agent_sprites[accused.getId()].drawTo(screen, position[0] + col_size - (agent_sprites[accused.getId()].getWidth() / cell_size), position[1])

                    # Draw text
                    text_x = (2 * position[0] + col_size) / 2  - (accusesText.get_width() / (cell_size * 2))
                    screen.blit(accusesText, (text_x * cell_size, position[1] * cell_size))
                    
            elif current_time < last_step_time + accusation_individual_time + accusation_ranking_time:
                pass # TODO: show accusation ranking popup.
            else:
                game.step()
        elif game.isVoting():
            # Blabla
            pass

        pygame.display.flip()

    pygame.quit()