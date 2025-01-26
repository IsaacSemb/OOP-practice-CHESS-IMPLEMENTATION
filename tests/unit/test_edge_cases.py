# tests/unit/test_edge_cases.py

from src.board.board import Board
from src.game.chess_game import ChessGame
from src.pieces.concrete_pieces import Bishop, King, Rook
from src.pieces.piece import Color, Position


def test_board_boundaries():
   board = Board()
   rook = Rook(Color.WHITE, Position('A', 1))
   
   # Test boundary movements
   moves = rook.get_possible_moves(board)
   assert Position('I', 1) not in moves  # Out of bounds
   assert Position('A', 9) not in moves  # Out of bounds
   assert Position('A', 0) not in moves  # Out of bounds

def test_pinned_piece():
   board = Board()
   king = King(Color.WHITE, Position('E', 1))
   bishop = Bishop(Color.WHITE, Position('E', 2))
   enemy_rook = Rook(Color.BLACK, Position('E', 8))
   
   board.place_piece(king, Position('E', 1))
   board.place_piece(bishop, Position('E', 2))
   board.place_piece(enemy_rook, Position('E', 8))
   
   # Bishop is pinned, shouldn't be able to move sideways
   moves = bishop.get_possible_moves(board)
   assert not any(pos.file != 'E' for pos in moves)

def test_multiple_checks():
   board = Board()
   king = King(Color.WHITE, Position('E', 4))
   enemy_rook1 = Rook(Color.BLACK, Position('E', 8))
   enemy_rook2 = Rook(Color.BLACK, Position('H', 4))
   
   board.place_piece(king, Position('E', 4))
   board.place_piece(enemy_rook1, Position('E', 8))
   board.place_piece(enemy_rook2, Position('H', 4))
   
   # King can only move diagonally to escape double check
   moves = king.get_possible_moves(board)
   assert all(abs(ord(pos.file) - ord('E')) == abs(pos.rank - 4) for pos in moves)

def test_piece_capture_own_color():
   board = Board()
   rook = Rook(Color.WHITE, Position('A', 1))
   own_pawn = Pawn(Color.WHITE, Position('A', 2))
   
   board.place_piece(rook, Position('A', 1))
   board.place_piece(own_pawn, Position('A', 2))
   
   moves = rook.get_possible_moves(board)
   assert Position('A', 2) not in moves

def test_en_passant_window():
   game = ChessGame()
   moves = [
       ('E2', 'E4'), ('A7', 'A6'),
       ('E4', 'E5'), ('D7', 'D5')
   ]
   for from_pos, to_pos in moves:
       game.move_piece(Position(*from_pos), Position(*to_pos))
       
   # Make an unrelated move
   game.move_piece(Position('A2'), Position('A3'))
   
   # En passant should no longer be possible
   pawn = game.board.get_piece_at(Position('E5'))
   moves = pawn.get_possible_moves(game.board)
   assert Position('D6') not in moves

def test_castling_through_check():
   game = ChessGame()
   # Clear pieces between king and rook
   game.board.remove_piece(Position('F', 1))
   game.board.remove_piece(Position('G', 1))
   
   # Add enemy rook attacking F1
   enemy_rook = Rook(Color.BLACK, Position('F', 8))
   game.board.place_piece(enemy_rook, Position('F', 8))
   
   # Castling through check should be invalid
   assert not game.move_piece(Position('E', 1), Position('G', 1))