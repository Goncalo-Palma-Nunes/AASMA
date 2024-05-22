from typing import Any
from environment import Game

import pygame
import math

class CellSprite:
    
    ###########################
    ###     Constructor     ###
    ###########################
    
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

    ###########################
    ### Getters and Setters ###
    ###########################
    
    def getImage(self):
        return self.image
    
    def getWidth(self):
        return self.image.get_width()
    
    def getHeight(self):
        return self.image.get_height()
    
    ###########################
    ###       Methods       ###
    ###########################

    def drawTo(self, surface, i, j):
        surface.blit(self.image, (i * self.cell_size + self.offset[0], j * self.cell_size + self.offset[1]))
        
    def drawToBigger(self, surface, i, j, scale):
        new_image = pygame.transform.scale(self.image, (self.cell_size * scale[0], self.cell_size * scale[1]))
        # Calculate the position to center the larger image
        new_offset_x = self.offset[0] - (self.cell_size * scale[0] // 2)
        new_offset_y = self.offset[1] - (self.cell_size * scale[1] // 2)
        surface.blit(new_image, (i * self.cell_size + new_offset_x, j * self.cell_size + new_offset_y))
        
        
class UI:
    
    ###########################
    ###     Constructor     ###
    ###########################
    
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
        self.popup = self.PopUp(self.board.getSize(), len(self.game.getAgents()), self.getCellSize())
    
    ###########################
    ###     Inner Class     ###
    ###########################
        
    class PopUp:
        
        ###########################
        ###     Constructor     ###
        ###########################
    
        def __init__(self, board_size, num_agents, cell_size):
            self.margin = 4
            self.row_size = 2
            self.col_size = 5 
            self.max_rows = board_size / self.row_size - self.margin
            self.cols = max(3, math.ceil(num_agents / self.max_rows) + 1)   
            self.rows = max(6, math.ceil(num_agents / self.cols))
            self.center = None
            self.box_size = None
            self.box_position = None
            self.box_size_background = None
            self.box_position_background = None
            self.cell_size = cell_size
            self.upper_box_position = None
        
        ###########################
        ### Getters and setters ###
        ###########################
            
        def getMargin(self):
            return self.margin  
        
        def getRowSize(self):
            return self.row_size
        
        def getColSize(self):
            return self.col_size
        
        def getMaxRows(self):
            return self.max_rows
        
        def getCols(self):
            return self.cols
        
        def getRows(self):
            return self.rows
        
        def setRows(self, rows):
            self.rows = rows
        
        def getCenter(self):
            return self.center
        
        def getBoxSize(self):
            return self.box_size
        
        def getBoxPosition(self):
            return self.box_position
        
        def getBoxSizeBackground(self):
            return self.box_size_background
        
        def getBoxPositionBackground(self):
            return self.box_position_background
        
        def getCellSize(self):
            return self.cell_size
        
        def getUpperBoxPosition(self):
            return self.upper_box_position
            
        ###########################
        ###       Methods       ###
        ###########################
        
        def drawBackground(self, board_size, screen):
            self.center = (board_size * self.getCellSize() / 2, board_size * self.getCellSize() / 2)
            self.box_size = (self.getCols() * self.getColSize() * self.getCellSize(), self.getRows() * self.getRowSize()  * self.getCellSize())
            self.box_position = (self.center[0] - self.box_size[0] / 2, self.center[1] - self.box_size[1] / 2)
            self.box_size_background = (self.getCols() * self.getColSize() * self.getCellSize() + (self.getRowSize() * self.getCellSize() / 3), self.getRows() * self.getRowSize() * self.getCellSize() + self.getRowSize() * self.getCellSize())
            self.box_position_background = (self.center[0] - self.box_size_background[0] / 2, self.center[1] - self.box_size_background[1] / 2 - (self.getRowSize() * self.getCellSize() / 3))
            
            pygame.draw.rect(screen, (161, 102, 47), (self.box_position_background, self.box_size_background))
            pygame.draw.rect(screen, (216, 181, 137), (self.box_position, self.box_size))
            
        def drawBackground2(self, board_size, screen, rows_background):
            self.center = (board_size * self.getCellSize() / 2, board_size * self.getCellSize() / 2)
            upper_box_size = (self.getCols() * self.getColSize() * self.getCellSize(), self.getRows() * self.getRowSize()  * self.getCellSize())
            self.upper_box_position = (self.center[0] - upper_box_size[0] /2, self.center[1] - upper_box_size[1])
            self.box_size = (self.getCols() * self.getColSize() * self.getCellSize(), self.getRows() * self.getRowSize()  * self.getCellSize())
            self.box_position = (self.center[0] - self.box_size[0] / 2, self.center[1])  
            self.box_size_background = (self.getCols() * self.getColSize() * self.getCellSize() + (self.getRowSize() * self.getCellSize() / 3), rows_background * self.getRowSize() * self.getCellSize() + self.getRowSize() * self.getCellSize())
            self.box_position_background = (self.center[0] - self.box_size_background[0] / 2, self.center[1] - self.box_size_background[1] / 2 - (self.getRowSize() * self.getCellSize() / 3))
            
            pygame.draw.rect(screen, (161, 102, 47), (self.box_position_background, self.box_size_background))
            pygame.draw.rect(screen, (216, 181, 137), (self.upper_box_position, upper_box_size))
            pygame.draw.rect(screen, (216, 181, 137), (self.box_position, self.box_size))
            
        def drawTitle(self, text, size, screen, pos1, pos2):
            new_font = pygame.font.SysFont("arialblack", size)
            text = new_font.render(text, True, (0,0,0))
            screen.blit(text, (pos1, pos2 + self.getRowSize() * self.getCellSize()/ 6))
            
        def drawBoxes(self, screen, i, j):
            small_box_size = (self.getColSize() * self.getCellSize(), self.getRowSize() * self.getCellSize())
            small_box_position = (self.getBoxPosition()[0] + i * self.getColSize() * self.getCellSize(), self.getBoxPosition()[1] + j * self.getRowSize() * self.getCellSize())
            pygame.draw.rect(screen, (161, 102, 47), (small_box_position, small_box_size), 1)
            
            return small_box_position
            
    ###########################
    ### Getters and Setters ###
    ###########################
    
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
        
    def getAppleSprite(self):
        return self.apple_sprite
        
    def setAppleSprite(self, cell_size, sprite_scale):
        self.apple_sprite = CellSprite.fromFile(cell_size, sprite_scale, "assets/apple.png")
        
    def getGrassSprite(self):    
        return self.grass_sprite
    
    def setGrassSprite(self, cell_size, sprite_scale):
        self.grass_sprite = CellSprite.fromFile(cell_size, sprite_scale, "assets/grass.png")
        
    def getJailSprite(self):    
        return self.jail_sprite

    def setJailSprite(self, cell_size, sprite_scale):
        self.jail_sprite = CellSprite.fromFile(cell_size, sprite_scale, "assets/jail.png")
        
    def getSlimeSprites(self):   
        return self.slime_sprites
    
    def setSlimeSprites(self, cell_size, sprite_scale):
        slime_sprites = {"blue": "slime_bluegreen.png", "gold": "slime_gold.png", "pink": "slime_pink.png", "purple": "slime_purple.png"}
        self.slime_sprites = {name: CellSprite.fromFile(cell_size, sprite_scale, f"assets/{path}") for (name, path) in slime_sprites.items()}
        
    def getHammerSprite(self): 
        return self.hammer_sprite
    
    def setHammerSprite(self, cell_size, sprite_scale):
        self.hammer_sprite = CellSprite.fromFile(cell_size, sprite_scale, "assets/hammer.png") 
    
    def getAgentSprites(self):
        return self.agent_sprites
        
    def setAgentSprites(self):
        for agent in self.getGame().getAgents():
            id_text = self.getFont().render(str(agent.getId()), True, (0, 0, 0))
    
            image_size = (max(self.getCellSize(), id_text.get_rect().width), self.getCellSize() + id_text.get_rect().height)
            image_offset = (min(0, self.getCellSize() - id_text.get_rect().width) / 2, -id_text.get_rect().height)

            image = pygame.Surface(image_size, pygame.SRCALPHA, 32)
            image.blit(self.getSlimeSprites()[agent.getColor()].getImage(), (-image_offset[0], -image_offset[1]))
            image.blit(id_text, ((image_size[0] - id_text.get_rect().width) / 2, 0))

            self.agent_sprites[agent.getId()] = CellSprite(self.getCellSize(), image, offset=(0, image_offset[1]))
    
    def getPopUp(self):
        return self.popup
    
    ###########################
    ###       Methods       ###
    ###########################
    
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
                        
        text = self.getFont().render(f"Round {self.getGame().getCurrentRound() + 1}", True, (0,0,0))
        self.getScreen().blit(text, (0, 0))           
                               
    def drawPopUpAccusationList(self):
        board_size = self.getBoard().getSize()
        pop_up = self.getPopUp()

        pop_up.drawBackground(board_size, self.getScreen())
        
        pop_up.drawTitle("Accusation List", self.getCellSize(), self.getScreen(), pop_up.getBoxPosition()[0], pop_up.getBoxPositionBackground()[1])
        accuses_text = self.getFont().render("accuses", True, (0, 0, 0))

        for player, accused in self.getGame().getAccusations().items():
            i = player.getId() // pop_up.getRows()
            j = player.getId() % pop_up.getRows()
            position = ((pop_up.getBoxPosition()[0] + i * pop_up.getColSize() * self.getCellSize()) / self.getCellSize(), (pop_up.getBoxPosition()[1] + j * pop_up.getRowSize() * self.getCellSize()) / self.getCellSize() + 1)
            
            # Draw accusation boxes
            pop_up.drawBoxes(self.getScreen(), i, j)
            
            # Draw player and accused sprites
            self.getAgentSprites()[player.getId()].drawTo(self.getScreen(), position[0], position[1])
            if accused is not None:
                self.getAgentSprites()[accused.getId()].drawTo(self.getScreen(), position[0] + pop_up.getColSize() - (self.getAgentSprites()[accused.getId()].getWidth() / self.getCellSize()), position[1])

            # Draw text
            text_x = (2 * position[0] + pop_up.getColSize()) / 2  - (accuses_text.get_width() / (self.getCellSize() * 2))
            self.getScreen().blit(accuses_text, (text_x * self.getCellSize(), position[1] * self.getCellSize()))
    
    def drawPopUpAccusationRanking(self):
        board_size = self.getBoard().getSize()
        pop_up = self.getPopUp()
        
        pop_up.setRows(max(6, math.ceil((len(self.getGame().getAgents())) / pop_up.getCols())) / 2)
        rows_background = max(6, math.ceil(len(self.getGame().getAgents()) / pop_up.getCols()))
        pop_up.drawBackground2(board_size, self.getScreen(), rows_background)
        pop_up.drawTitle("Accusation Ranking", self.getCellSize(), self.getScreen(), pop_up.getUpperBoxPosition()[0], pop_up.getBoxPositionBackground()[1])
        
        new_font = pygame.font.SysFont("arialblack", self.getCellSize())
        
        for rank in range(1, len(self.getGame().getOrderedAccusedList()) + 1):
            rows = math.floor(pop_up.getRows())
            player_tuple = list(self.getGame().getOrderedAccusedList().items())[rank-1]
            i = (rank-2) // rows
            j = (rank-2) % rows

            text = f"Top {rank}: {player_tuple[1]} votes"
            if i > pop_up.getCols() -1 or player_tuple[0] is None:
                break
            elif rank == 1:
                # Draw player and hammer sprite
                position = (pop_up.getCenter()[0] / self.getCellSize(), ((pop_up.getUpperBoxPosition()[1] + pop_up.getBoxPosition()[1]) /2) / self.getCellSize())
                self.getAgentSprites()[player_tuple[0].getId()].drawToBigger(self.getScreen(), position[0], position[1], (2, 3.5))
                self.hammer_sprite.drawTo(self.getScreen(), position[0] + self.getAgentSprites()[player_tuple[0].getId()].getWidth() / self.getCellSize(), position[1] - self.getAgentSprites()[player_tuple[0].getId()].getHeight() / self.getCellSize())
                
                # Draw text
                rank_text = new_font.render(text, True, (0,0,0))
                self.getScreen().blit(rank_text, ((position[0] - (rank_text.get_width() / (self.getCellSize() * 2))) * self.getCellSize(), (position[1] + self.getCellSize() / self.getCellSize()) * self.getCellSize()))
            else:
                # Draw player sprites
                position = ((pop_up.getBoxPosition()[0] + i * pop_up.getColSize() * self.getCellSize()) / self.getCellSize(), (pop_up.getBoxPosition()[1] + j * pop_up.getRowSize() * self.getCellSize()) / self.getCellSize() + 1)
                self.getAgentSprites()[player_tuple[0].getId()].drawTo(self.getScreen(), position[0] + pop_up.getColSize() - (self.getAgentSprites()[player_tuple[0].getId()].getWidth() * 2/ self.getCellSize()), position[1])
                
                # Draw voting boxes
                small_box_position = pop_up.drawBoxes(self.getScreen(), i, j)

                # Draw text
                rank_font = pygame.font.SysFont("arialblack", 10 * self.getCellSize() // 25)    
                rank_text = rank_font.render(text, True, (0,0,0))
                self.getScreen().blit(rank_text, (small_box_position[0], small_box_position[1]))
                
    def drawPopUpVotingList(self):      
        board_size = self.getBoard().getSize()
        pop_up = self.getPopUp()
        
        pop_up.setRows(max(6, math.ceil((len(self.getGame().getAgents())) / pop_up.getCols())))
        pop_up.drawBackground(board_size, self.getScreen())
        pop_up.drawTitle("Voting List", self.getCellSize(), self.getScreen(), pop_up.getBoxPosition()[0], pop_up.getBoxPositionBackground()[1])

        for player, vote in self.getGame().getVotes().items():
            i = player.getId() // pop_up.getRows()
            j = player.getId() % pop_up.getRows()
            position = ((pop_up.getBoxPosition()[0] + i * pop_up.getColSize() * self.getCellSize()) / self.getCellSize(), (pop_up.getBoxPosition()[1] + j * pop_up.getRowSize() * self.getCellSize()) / self.getCellSize() + 1)
            
            # Draw accusation boxes
            pop_up.drawBoxes(self.getScreen(), i, j)
                    
            # Draw player sprite
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
        board_size = self.getBoard().getSize()
        pop_up = self.getPopUp()
        
        pop_up.drawBackground(board_size, self.getScreen())
        pop_up.drawTitle("Voting Result", self.getCellSize(), self.getScreen(), pop_up.getBoxPosition()[0], pop_up.getBoxPositionBackground()[1])
        
        new_font = pygame.font.SysFont("arialblack", self.getCellSize())
        votes = self.getGame().getNumberOfVotes()
        
        # Draw accused sprite
        accused = self.getGame().getMostAccused()
        position = (pop_up.getCenter()[0] / self.getCellSize(), pop_up.getCenter()[1] / self.getCellSize())
        self.getAgentSprites()[accused.getId()].drawToBigger(self.getScreen(), position[0], position[1], (2, 3.5))
        
        # Draw ban text
        ban_font = pygame.font.SysFont("arialblack", self.getCellSize() * 3 // 2)
        ban_text = ban_font.render("Ban?", True, (0,0,0))
        ban_text_x = position[0] - (ban_text.get_width() / (self.getCellSize() * 2))
        ban_text_y = position[1] - self.getAgentSprites()[accused.getId()].getHeight() * 3 / self.getCellSize()
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
        
    def drawGameOver(self):
        pop_up = self.getPopUp()
        new_font = pygame.font.SysFont("arialblack", self.getCellSize() * 2)
        
        position = (pop_up.getCenter()[0] / self.getCellSize(), pop_up.getCenter()[1] / self.getCellSize())
        text = new_font.render("GAME OVER", True, (0,0,0))
        text_x = position[0]  - (text.get_width() / (self.getCellSize() * 2))
        text_y = position[1] - (text.get_height() / (self.getCellSize() * 2))
        self.getScreen().blit(text, (text_x * self.getCellSize(), text_y * self.getCellSize()))
        
        