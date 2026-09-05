import chess
import pygame
import pygame.gfxdraw

LIGHT_SQUARE = (240, 217, 181) 
DARK_SQUARE = (181, 136, 99)
HIGHLIGHT = (158, 158,158, 158)
SQ_SIZE = 64

class Board:
    def __init__(self):
        self.board = chess.Board()
        self.colors = [LIGHT_SQUARE, DARK_SQUARE]
        self.images = {}

        self.sound_move = None
        self.sound_capture = None
        self.load_assets()
    
    def load_assets(self):
        pieces = ['P', 'R', 'N', 'B', 'Q', 'K', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']

        for piece in pieces:
            img = pygame.image.load(f'images/' + piece + '.png')
            img = pygame.transform.scale(img, (SQ_SIZE, SQ_SIZE))
            self.images[piece] = img

        pygame.mixer.init()
        self.sound_move = pygame.mixer.Sound("sounds/Move.mp3")
        self.sound_capture = pygame.mixer.Sound("sounds/Capture.mp3")

    def draw(self, screen):
        for r in range(8):
            for c in range(8):
                col = self.colors[(r + c) % 2]
                pygame.draw.rect(screen, col, pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


    def draw_pieces(self, screen):
        for sq in chess.SQUARES:
            piece = self.board.piece_at(sq)

            if piece:
                col = chess.square_file(sq)
                row = 7 - chess.square_rank(sq)

                if piece.color == chess.WHITE:
                    c = piece.symbol().upper()
                else:
                    c = 'b' + piece.symbol().upper()

                screen.blit(self.images[c], (col * SQ_SIZE, row * SQ_SIZE))
    
    def highlight_check(self, screen):
        if self.board.is_check():

            king_square = self.board.king(self.board.turn)
        
            col = chess.square_file(king_square)
            row = 7 - chess.square_rank(king_square)
        

            red_surface = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
            red_surface.fill((255, 0, 0, 100))
        
            screen.blit(red_surface, (col * SQ_SIZE, row * SQ_SIZE))

    def highlight_last_move(self, screen):
        if self.board.move_stack:
            last_move = self.board.peek()
        
            squares = [last_move.from_square, last_move.to_square]
        
            for sq in squares:
                col = chess.square_file(sq)
                row = 7 - chess.square_rank(sq)
            
                move_surface = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
                move_surface.fill((170, 190, 80, 130))
            
                screen.blit(move_surface, (col * SQ_SIZE, row * SQ_SIZE))
    
    def highlight_possible_moves(self, screen, selected):
        s = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
        center = (SQ_SIZE // 2, SQ_SIZE // 2)
        r = SQ_SIZE // 5

        pygame.gfxdraw.aacircle(s, center[0], center[1], r, HIGHLIGHT)
        pygame.gfxdraw.filled_circle(s, center[0], center[1], r, HIGHLIGHT)

        moves = [move for move in self.board.legal_moves if move.from_square == selected]
    
        for move in moves:
            col = chess.square_file(move.to_square)
            row = 7 - chess.square_rank(move.to_square)

            screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))

    def highlight(self, screen, selected):
        self.highlight_check(screen)
        self.highlight_last_move(screen)

        if selected is None:
            return
        
        self.highlight_possible_moves(screen, selected)

    def sound(self, move):
        if self.board.is_capture(move):
            self.sound_capture.play()
        else:
            self.sound_move.play()

    def turn(self):
        return self.board.turn
    
    def is_game_over(self):
        return self.board.is_game_over()
