# tests/unit/test_piece_movement.py
import pytest
from src.game.validation import MoveValidator
from src.pieces.concrete_pieces import Rook, Knight, Bishop, Queen, King, Pawn
from src.pieces.piece import Color, Position
from src.board.board import Board

@pytest.fixture
def empty_board():
    return Board()

def test_rook_movement(empty_board):
    rook = Rook(Color.WHITE, Position('A', 1))
    empty_board.place_piece(rook, Position('A', 1))
    
    moves = rook.get_possible_moves(empty_board)
    expected_positions = [
        Position('A', i) for i in range(2, 9)
    ] + [Position(chr(ord('A') + i), 1) for i in range(1, 8)]
    
    assert set(moves) == set(expected_positions)

def test_blocked_rook(empty_board):
    rook = Rook(Color.WHITE, Position('A', 1))
    blocking_piece = Pawn(Color.WHITE, Position('A', 2))
    
    empty_board.place_piece(rook, Position('A', 1))
    empty_board.place_piece(blocking_piece, Position('A', 2))
    
    moves = rook.get_possible_moves(empty_board)
    expected_positions = [Position(chr(ord('A') + i), 1) for i in range(1, 8)]
    
    assert set(moves) == set(expected_positions)
    
    # tests/unit/test_piece_movement.py (continued)

def test_knight_movement(empty_board):
   knight = Knight(Color.WHITE, Position('B', 1))
   empty_board.place_piece(knight, Position('B', 1))
   
   moves = knight.get_possible_moves(empty_board)
   expected_positions = {Position('A', 3), Position('C', 3), Position('D', 2)}
   
   assert set(moves) == expected_positions

def test_pawn_first_move(empty_board):
   pawn = Pawn(Color.WHITE, Position('E', 2))
   empty_board.place_piece(pawn, Position('E', 2))
   
   moves = pawn.get_possible_moves(empty_board)
   expected_positions = {Position('E', 3), Position('E', 4)}
   
   assert set(moves) == expected_positions

def test_pawn_capture(empty_board):
   pawn = Pawn(Color.WHITE, Position('E', 2))
   enemy_pawn = Pawn(Color.BLACK, Position('F', 3))
   
   empty_board.place_piece(pawn, Position('E', 2))
   empty_board.place_piece(enemy_pawn, Position('F', 3))
   
   moves = pawn.get_possible_moves(empty_board)
   assert Position('F', 3) in moves

def test_king_castling(empty_board):
   king = King(Color.WHITE, Position('E', 1))
   rook = Rook(Color.WHITE, Position('H', 1))
   
   empty_board.place_piece(king, Position('E', 1))
   empty_board.place_piece(rook, Position('H', 1))
   
   moves = king.get_possible_moves(empty_board)
   assert Position('G', 1) in moves

def test_queen_diagonal_and_straight(empty_board):
   queen = Queen(Color.WHITE, Position('D', 4))
   empty_board.place_piece(queen, Position('D', 4))
   
   moves = queen.get_possible_moves(empty_board)
   
   # Test diagonals
   diagonals = {Position('C', 3), Position('E', 5), Position('C', 5), Position('E', 3)}
   # Test straight
   straight = {Position('D', 5), Position('D', 3), Position('E', 4), Position('C', 4)}
   
   assert diagonals.issubset(set(moves))
   assert straight.issubset(set(moves))

# Add game state tests
def test_check_detection():
   board = Board()
   king = King(Color.WHITE, Position('E', 1))
   enemy_rook = Rook(Color.BLACK, Position('E', 8))
   
   board.place_piece(king, Position('E', 1))
   board.place_piece(enemy_rook, Position('E', 8))
   
   validator = MoveValidator(board)
   assert validator._is_king_in_check(Color.WHITE)