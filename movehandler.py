import pygame
import chess

SQ_SIZE = 64

class MoveHandler:
    def __init__(self):
        self.selected = None

    def handle_mouse(self, board):
        x, y = pygame.mouse.get_pos()

        row = y // SQ_SIZE
        col = x // SQ_SIZE  

        square = chess.square(col, 7 - row)

        if self.selected is not None:
            move = chess.Move(self.selected, square)
            queen_promo = chess.Move(self.selected, square, promotion=chess.QUEEN)

            if queen_promo in board.board.legal_moves:

                board.sound(queen_promo)
                board.board.push(queen_promo)

            elif move in board.board.legal_moves:

                board.sound(move)
                board.board.push(move)

            self.selected = None
        else:
            piece = board.board.piece_at(square)
            if piece:
                self.selected = square