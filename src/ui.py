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
        
    def drawToBigger(self, surface, i, j, scale):
        new_image = pygame.transform.scale(self.image, (self.cell_size * scale[0], self.cell_size * scale[1]))
        # Calculate the position to center the larger image
        new_offset_x = self.offset[0] - (self.cell_size * scale[0] // 2)
        new_offset_y = self.offset[1] - (self.cell_size * scale[1] // 2)
        surface.blit(new_image, (i * self.cell_size + new_offset_x, j * self.cell_size + new_offset_y))
        
        
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
        self.setHammerSprite(cell_size, sprite_scale)
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
    
    def setHammerSprite(self, cell_size, sprite_scale):
        self.hammer_sprite = CellSprite.fromFile(cell_size, sprite_scale, "assets/hammer.png") 
    
    def getHammerSprite(self): 
        return self.hammer_sprite
        
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
        accuses_text = self.getFont().render("accuses", True, (0, 0, 0))
        accusation_text = new_font.render("Accusation List", True, (0,0,0))

        self.getScreen().blit(accusation_text, (box_position[0], box_position_background[1] + row_size * self.getCellSize()/ 6))

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
            text_x = (2 * position[0] + col_size) / 2  - (accuses_text.get_width() / (self.getCellSize() * 2))
            self.getScreen().blit(accuses_text, (text_x * self.getCellSize(), position[1] * self.getCellSize()))
    
    def drawPopUpAccusationRanking(self):
        margin = 4
        row_size = 2
        col_size = 5
        
        board_size = self.getBoard().getSize()
        max_rows = board_size / row_size - margin

        cols = len(self.getGame().getAgents()) // max_rows + 1
        rows_background = len(self.getGame().getAgents()) // cols
        rows = (len(self.getGame().getAgents()) /2) // cols

        center = (board_size * self.getCellSize() / 2, board_size * self.getCellSize() / 2)
        upper_box_size = (cols * col_size * self.getCellSize(), rows * row_size * self.getCellSize())
        upper_box_position = (center[0] - upper_box_size[0] /2, center[1] - upper_box_size[1])
        
        bottom_box_size = (cols * col_size * self.getCellSize(), rows * row_size * self.getCellSize())
        bottom_box_position = (center[0] - upper_box_size[0] /2, center[1])        
        
        box_size_background = (cols * col_size * self.getCellSize() + (row_size * self.getCellSize() /3), rows_background * row_size * self.getCellSize() + row_size * self.getCellSize())
        box_position_background = (center[0] - box_size_background[0] / 2, center[1] - box_size_background[1] / 2 - (row_size * self.getCellSize() / 3))
        
        pygame.draw.rect(self.getScreen(), (161, 102, 47), (box_position_background, box_size_background))
        pygame.draw.rect(self.getScreen(), (216, 181, 137), (upper_box_position, upper_box_size))
        pygame.draw.rect(self.getScreen(), (216, 181, 137), (bottom_box_position, bottom_box_size))
        
        new_font = pygame.font.SysFont("arialblack", self.getCellSize())
        accusation_text = new_font.render("Accusation Ranking", True, (0,0,0))
        
        self.getScreen().blit(accusation_text, (upper_box_position[0], box_position_background[1] + row_size * self.getCellSize()/ 6))
        
        for rank in range(1, len(self.getGame().getOrderedAccusedList())):
            player_tuple = list(self.getGame().getOrderedAccusedList().items())[rank-1]
            i = (rank-2) // rows
            j = (rank-2) % rows
            text = f"Top {rank}: {player_tuple[1]} votes"
            if i > rows -1 or j > rows -1:
                break
            elif rank == 1:
                # Draw player and hammer sprite
                position = (center[0] / self.getCellSize(), ((upper_box_position[1] + bottom_box_position[1]) /2) / self.getCellSize())
                self.getAgentSprites()[player_tuple[0].getId()].drawToBigger(self.getScreen(), position[0], position[1], (2, 3.5))
                self.hammer_sprite.drawTo(self.getScreen(), position[0] + self.getAgentSprites()[player_tuple[0].getId()].getWidth() / self.getCellSize(), position[1] - self.getAgentSprites()[player_tuple[0].getId()].getHeight() / self.getCellSize())
                
                # Draw text
                rank_text = new_font.render(text, True, (0,0,0))
                self.getScreen().blit(rank_text, ((position[0] - (rank_text.get_width() / (self.getCellSize() * 2))) * self.getCellSize(), (position[1] + self.getCellSize() / self.getCellSize()) * self.getCellSize()))
            else:
                # Draw player sprites
                position = ((bottom_box_position[0] + i * col_size * self.getCellSize()) / self.getCellSize(), (bottom_box_position[1] + j * row_size * self.getCellSize()) / self.getCellSize() + 1)
                self.getAgentSprites()[player_tuple[0].getId()].drawTo(self.getScreen(), position[0] + col_size - (self.getAgentSprites()[player_tuple[0].getId()].getWidth() * 2/ self.getCellSize()), position[1])
                
                # Draw voting boxes
                voting_box_size = (col_size * self.getCellSize(), row_size * self.getCellSize())
                voting_box_position = (bottom_box_position[0] + i * col_size * self.getCellSize(), bottom_box_position[1] + j * row_size * self.getCellSize())
                pygame.draw.rect(self.getScreen(), (161, 102, 47), (voting_box_position, voting_box_size), 1)

                # Draw text
                rank_font = pygame.font.SysFont("arialblack", 10 * self.getCellSize() // 25)    
                rank_text = rank_font.render(text, True, (0,0,0))
                self.getScreen().blit(rank_text, (voting_box_position[0], voting_box_position[1]))
                
    def drawPopUpVotingList(self):
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
        voting_text = new_font.render("Voting List", True, (0,0,0))

        self.getScreen().blit(voting_text, (box_position[0], box_position_background[1] + row_size * self.getCellSize()/ 6))

        for player, vote in self.getGame().getVotes().items():
            i = player.getId() // rows
            j = player.getId() % rows
            position = ((box_position[0] + i * col_size * self.getCellSize()) / self.getCellSize(), (box_position[1] + j * row_size * self.getCellSize()) / self.getCellSize() + 1)
                    
            # Draw accusation boxes
            accusation_box_size = (col_size * self.getCellSize(), row_size * self.getCellSize())
            accusation_box_position = (box_position[0] + i * col_size * self.getCellSize(), box_position[1] + j * row_size * self.getCellSize())
            pygame.draw.rect(self.getScreen(), (161, 102, 47), (accusation_box_position, accusation_box_size), 1)
                    
            # Draw player and accused sprites
            self.getAgentSprites()[player.getId()].drawTo(self.getScreen(), position[0], position[1])

            # Draw text
            if vote == True:
                text = "yes"
            else:
                text = "no"
            accuses_text = self.getFont().render(f"votes {text}", True, (0, 0, 0))
            text_x = position[0] + self.getAgentSprites()[player.getId()].getWidth() / self.getCellSize()
            self.getScreen().blit(accuses_text, ((text_x + 0.25) * self.getCellSize(), position[1] * self.getCellSize()))
    
    def drawPopUpVotingResult(self):
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
        
        votes = self.getGame().getNumberOfVotes()
        new_font = pygame.font.SysFont("arialblack", self.getCellSize())
        voting_text = new_font.render("Final Voting Result", True, (0,0,0))

        self.getScreen().blit(voting_text, (box_position[0], box_position_background[1] + row_size * self.getCellSize()/ 6))
        
        # Draw accused sprite
        accused = self.getGame().getMostAccused()
        position = (center[0] / self.getCellSize(), center[1] / self.getCellSize())
        self.getAgentSprites()[accused.getId()].drawToBigger(self.getScreen(), position[0], position[1], (2, 3.5))
        
        # Draw ban text
        ban_font = pygame.font.SysFont("arialblack", self.getCellSize() * 3 // 2)
        ban_text = ban_font.render("Should he be banned?", True, (0,0,0))
        ban_text_x = position[0] - (ban_text.get_width() / (self.getCellSize() * 2))
        ban_text_y = position[1] - self.getAgentSprites()[accused.getId()].getHeight() * 4 / self.getCellSize()
        self.getScreen().blit(ban_text, (ban_text_x * self.getCellSize(), ban_text_y * self.getCellSize()))

        # Draw voting results text
        votes_text = new_font.render(f"YES: {votes[0]} NO: {votes[1]}", True, (0,0,0))
        votes_text_x = position[0]  - (votes_text.get_width() / (self.getCellSize() * 2))
        votes_text_y = position[1] + self.getAgentSprites()[accused.getId()].getHeight() / self.getCellSize()
        self.getScreen().blit(votes_text, (votes_text_x * self.getCellSize(), votes_text_y * self.getCellSize()))
        
        # Decide if the accused is guilty or innocent     
        if votes[0] > votes[1]:
            text = f"Sir {accused.getId()} is guilty!"
            self.getJailSprite().drawToBigger(self.getScreen(), position[0], position[1], (2, 2))
        else:
            text = f"Sir {accused.getId()} is innocent!"
        
        # Draw result text    
        result_text = new_font.render(text, True, (0,0,0))
        result_text_x = position[0]  - (result_text.get_width() / (self.getCellSize() * 2))
        result_text_y = votes_text_y + result_text.get_height() / self.getCellSize()
        self.getScreen().blit(result_text, (result_text_x * self.getCellSize(), result_text_y * self.getCellSize()))
        
        