from typing import Any
from environment import Game

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
        
class UI:
    def __init__(self, game, screen, cell_size, sprite_scale):
        self.board = game.getBoard()
        self.screen = screen
        self.cell_size = cell_size
        self.game = game
        self.font = pygame.font.SysFont("arialblack", cell_size //2)
        self.setAppleSprite(cell_size, sprite_scale)
        self.setGrassSprite(cell_size, sprite_scale)
        self.setJailSprite(cell_size, sprite_scale)
        self.setSlimeSprites(cell_size, sprite_scale)
        self.agent_sprites = {}
        
    def getBoard(self):
        return self.board
    
    def getScreen(self):
        return self.screen
    
    def getCellSize(self):
        return self.cell_size
    
    def getGame(self):
        return self.game
    
    def getFont(self):
        return self.font
    
    def setFont(self, font):
        self.font = font
        
    def setAppleSprite(self, cell_size, sprite_scale):
        self.apple_sprite = CellSprite.fromFile(cell_size, sprite_scale, "assets/apple.png")
        
    def getAppleSprite(self):
        return self.apple_sprite
    
    def setGrassSprite(self, cell_size, sprite_scale):
        self.grass_sprite = CellSprite.fromFile(cell_size, sprite_scale, "assets/grass.png")
        
    def getGrassSprite(self):    
        return self.grass_sprite

    def setJailSprite(self, cell_size, sprite_scale):
        self.jail_sprite = CellSprite.fromFile(cell_size, sprite_scale, "assets/jail.png")
    
    def getJailSprite(self):    
        return self.jail_sprite
    
    def setSlimeSprites(self, cell_size, sprite_scale):
        slime_sprites = ["slime_bluegreen.png", "slime_gold.png", "slime_pink.png", "slime_purple.png"]
        self.slime_sprites = [CellSprite.fromFile(cell_size, sprite_scale, f"assets/{name}") for name in slime_sprites]
    
    def getSlimeSprites(self):   
        return self.slime_sprites
        
    def setAgentSprites(self):
        for agent in self.getGame().getAgents():
            id_text = self.getFont().render(str(agent.getId()), True, (0, 0, 0))
    
            image_size = (max(self.getCellSize(), id_text.get_rect().width), self.getCellSize() + id_text.get_rect().height)
            image_offset = (min(0, self.getCellSize() - id_text.get_rect().width) / 2, -id_text.get_rect().height)

            image = pygame.Surface(image_size, pygame.SRCALPHA, 32)
            image.blit(self.getSlimeSprites()[0].getImage(), (-image_offset[0], -image_offset[1]))
            image.blit(id_text, ((image_size[0] - id_text.get_rect().width) / 2, 0))

            self.agent_sprites[agent.getId()] = CellSprite(self.getCellSize(), image, offset=(0, image_offset[1]))
            
    def getAgentSprites(self):
        return self.agent_sprites
    
    def drawBoard(self):
        for i in range(self.getBoard().getSize()):
            for j in range(self.getBoard().getSize()):

                cell = self.getBoard().getCell(i, j)
                self.getGrassSprite().drawTo(self.getScreen(), i, j)

                if cell.hasResource():
                    self.getAppleSprite().drawTo(self.getScreen(), i, j)
                if cell.hasAgent():
                    self.getAgentSprites()[cell.getAgent().getId()].drawTo(self.getScreen(), i, j)
                    if cell.getAgent() == self.getGame().getImprisoned():
                        self.getJailSprite().drawTo(self.getScreen(), i, j)
                        
    def drawPopUpAccusationList(self):
        margin = 4
        row_size = 2
        col_size = 5
        
        board_size = self.getBoard().getSize()
        max_rows = board_size / row_size - margin

        cols = len(self.getGame().getAgents()) // max_rows + 1
        rows = len(self.getGame().getAgents()) // cols

        center = (board_size * self.getCellSize() / 2, board_size * self.getCellSize() / 2)
        box_size = (cols * col_size * self.getCellSize(), rows * row_size * self.getCellSize())
        box_position = (center[0] - box_size[0] / 2, center[1] - box_size[1] / 2)
                
        box_size_background = (cols * col_size * self.getCellSize() + (row_size * self.getCellSize() /3), rows * row_size * self.getCellSize() + row_size * self.getCellSize())
        box_position_background = (center[0] - box_size_background[0] / 2, center[1] - box_size_background[1] / 2 - (row_size * self.getCellSize() / 3))
        
        pygame.draw.rect(self.getScreen(), (161, 102, 47), (box_position_background, box_size_background))
        pygame.draw.rect(self.getScreen(), (216, 181, 137), (box_position, box_size))
                
        new_font = pygame.font.SysFont("arialblack", self.getCellSize())
        accusesText = self.getFont().render("accuses", True, (0, 0, 0))
        accusationText = new_font.render("Accusation List", True, (0,0,0))

                
        self.getScreen().blit(accusationText, (box_position[0], box_position_background[1] + row_size * self.getCellSize()/ 6))

        for player, accused in self.getGame().getAccusations().items():
            i = player.getId() // rows
            j = player.getId() % rows
            position = ((box_position[0] + i * col_size * self.getCellSize()) / self.getCellSize(), (box_position[1] + j * row_size * self.getCellSize()) / self.getCellSize() + 1)
                    
            # Draw accusation boxes
            accusation_box_size = (col_size * self.getCellSize(), row_size * self.getCellSize())
            accusation_box_position = (box_position[0] + i * col_size * self.getCellSize(), box_position[1] + j * row_size * self.getCellSize())
            pygame.draw.rect(self.getScreen(), (161, 102, 47), (accusation_box_position, accusation_box_size), 1)
                    
            # Draw player and accused sprites
            self.getAgentSprites()[player.getId()].drawTo(self.getScreen(), position[0], position[1])
            self.getAgentSprites()[accused.getId()].drawTo(self.getScreen(), position[0] + col_size - (self.getAgentSprites()[accused.getId()].getWidth() / self.getCellSize()), position[1])

            # Draw text
            text_x = (2 * position[0] + col_size) / 2  - (accusesText.get_width() / (self.getCellSize() * 2))
            self.getScreen().blit(accusesText, (text_x * self.getCellSize(), position[1] * self.getCellSize()))
        
        
