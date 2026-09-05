import chess
import pygame
import bot
from board import Board
from movehandler import MoveHandler

pause = 1000

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((512, 512))
        self.clock = pygame.time.Clock()
        self.move_handler = MoveHandler()

        self.game = True
        self.wait = 0
        self.board = Board()

    def handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.move_handler.handle_mouse(self.board)
    
    def update(self):
        if self.board.turn() == chess.BLACK and not self.board.is_game_over():
            if self.wait == 0:
                self.wait = pygame.time.get_ticks()

            if pygame.time.get_ticks() - self.wait > pause:

                bot_move = bot.get_bot_move(self.board.board)

                self.board.sound(bot_move)
            
                self.board.board.push(bot_move)
                self.wait = 0
    
    def render(self):
        self.board.draw(self.screen)
        self.board.highlight(self.screen, self.move_handler.selected)
        self.board.draw_pieces(self.screen)

        pygame.display.flip()
        pass
   
    def run(self):

        while self.game:

            self.handle()
            self.update()
            self.render()
            self.clock.tick(60)

        pygame.quit()
        pass
