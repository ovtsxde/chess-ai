import torch
import torch.nn as nn
import chess
import numpy as np

class ChessNet(nn.Module):
    def __init__(self):
        super(ChessNet, self).__init__()
        self.conv1 = nn.Conv2d(12, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(128, 128, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(128 * 8 * 8, 1024)
        self.fc2 = nn.Linear(1024, 4096)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = torch.relu(self.conv3(x))
        x = x.view(-1, 128 * 8 * 8)
        x = torch.relu(self.fc1(x))
        return self.fc2(x)


def board_to_matrix(board):
    matrix = np.zeros((12, 8, 8), dtype = np.float32)
    piece_map = board.piece_map()
    for square, piece in piece_map.items():
        row = 7 - (square // 8)
        col = square % 8
        piece_type = piece.piece_type - 1
        if not piece.color:
            piece_type += 6
        matrix[piece_type, row, col] = 1.0
    return matrix

model = ChessNet()

model.load_state_dict(torch.load("chess_bot.pth", map_location="cpu"))
model.eval()

def get_bot_move(board):

    matrix = board_to_matrix(board)
    input_tensor = torch.tensor(np.array([matrix]), dtype = torch.float32)
    
    with torch.no_grad():
        predictions = model(input_tensor).cpu().numpy()[0]

    best_move_indices = np.argsort(predictions)[::-1]
    
    for move_idx in best_move_indices:
        from_square = move_idx // 64
        to_square = move_idx % 64
        
        move = chess.Move(from_square, to_square)
        
        queen_promotion_move = chess.Move(from_square, to_square, promotion = chess.QUEEN)

        if queen_promotion_move in board.legal_moves:
             return queen_promotion_move

        if move in board.legal_moves:
            return move
    