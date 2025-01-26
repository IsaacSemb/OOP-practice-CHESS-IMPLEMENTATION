# src/game/game_cli.py

from src.game.chess_game import ChessGame
from src.pieces.piece import Color, Position


class ChessGameCLI:
    def __init__(self):
        self.game = ChessGame()

    def display_board(self):
        print("\n  A B C D E F G H")
        for rank in range(8, 0, -1):
            row = f"{rank} "
            for file in 'ABCDEFGH':
                piece = self.game.board.get_piece_at(Position(file, rank))
                symbol = self._get_piece_symbol(piece)
                row += symbol + " "
            print(row + f"{rank}")
        print("  A B C D E F G H\n")

    def _get_piece_symbol(self, piece):
        if not piece:
            return "."
        
        symbols = {
            'King': 'K', 'Queen': 'Q', 'Rook': 'R',
            'Bishop': 'B', 'Knight': 'N', 'Pawn': 'P'
        }
        symbol = symbols[piece.__class__.__name__]
        return symbol if piece.color == Color.WHITE else symbol.lower()

    def play(self):
        while True:
            self.display_board()
            try:
                from_pos = input("From (e.g. E2): ").upper()
                if from_pos == 'Q':
                    break
                to_pos = input("To (e.g. E4): ").upper()
                
                success = self.game.move_piece(
                    Position(from_pos[0], int(from_pos[1])),
                    Position(to_pos[0], int(to_pos[1]))
                )
                
                if not success:
                    print("Invalid move!")
                    
            except (ValueError, IndexError):
                print("Invalid input! Use format: E2")

if __name__ == "__main__":
    game = ChessGameCLI()
    game.play()