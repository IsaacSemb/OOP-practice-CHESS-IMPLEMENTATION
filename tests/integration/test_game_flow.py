# tests/integration/test_game_flow.py
import pytest
from src.board.board import Board
from src.game.chess_game import ChessGame
from src.pieces.concrete_pieces import King, Queen
from src.pieces.piece import Color, Position

def test_complete_game():
    game = ChessGame()
    
    # Test scholars mate
    moves = [
        ('E2', 'E4'), ('E7', 'E5'),
        ('F1', 'C4'), ('B8', 'C6'),
        ('D1', 'H5'), ('G8', 'F6'),
        ('H5', 'F7')
    ]
    
    for from_pos, to_pos in moves[:-1]:
        assert game.move_piece(Position(*from_pos), Position(*to_pos))
        
    # Final checkmate move
    assert game.move_piece(Position(*moves[-1][0]), Position(*moves[-1][1]))
    assert game._game_state == 'CHECKMATE'
    
    
# tests/integration/test_game_flow.py

def test_castling_kingside():
   game = ChessGame()
   # Clear pieces between king and rook
   game.board.remove_piece(Position('F', 1))
   game.board.remove_piece(Position('G', 1))
   
   assert game.move_piece(Position('E', 1), Position('G', 1))
   assert game.board.get_piece_at(Position('F', 1)) is not None  # Rook moved

def test_castling_blocked():
   game = ChessGame()
   # Keep blocking piece
   assert not game.move_piece(Position('E', 1), Position('G', 1))

def test_en_passant():
   game = ChessGame()
   moves = [
       ('E2', 'E4'), ('A7', 'A6'),
       ('E4', 'E5'), ('D7', 'D5')
   ]
   for from_pos, to_pos in moves:
       game.move_piece(Position(*from_pos), Position(*to_pos))
   
   # En passant capture
   assert game.move_piece(Position('E5'), Position('D6'))
   assert game.board.get_piece_at(Position('D5')) is None

def test_pawn_promotion():
   game = ChessGame()
   # Move pawn to promotion square
   pawn = game.board.get_piece_at(Position('E', 2))
   game.board.move_piece(Position('E', 2), Position('E', 7))
   
   assert game.move_piece(Position('E', 7), Position('E', 8), Queen)
   promoted_piece = game.board.get_piece_at(Position('E', 8))
   assert isinstance(promoted_piece, Queen)

def test_stalemate():
   game = ChessGame()
   # Clear board except kings
   game.board = Board()
   game.board.place_piece(King(Color.WHITE, Position('A', 1)), Position('A', 1))
   game.board.place_piece(King(Color.BLACK, Position('C', 2)), Position('C', 2))
   
   assert game._is_stalemate()

def test_invalid_moves():
   game = ChessGame()
   invalid_moves = [
       # Move to same square
       ('E2', 'E2'),
       # Move opponent's piece
       ('E7', 'E6'),
       # Move through pieces
       ('B1', 'B3'),
       # Invalid piece movement
       ('A2', 'A5')
   ]
   
   for from_pos, to_pos in invalid_moves:
       assert not game.move_piece(Position(*from_pos), Position(*to_pos))

def test_check_evasion():
   game = ChessGame()
   moves = [
       ('E2', 'E4'), ('E7', 'E5'),
       ('F1', 'C4'), ('G8', 'F6'),
       ('D1', 'H5')
   ]
   for from_pos, to_pos in moves:
       game.move_piece(Position(*from_pos), Position(*to_pos))
   
   # Black must block check
   assert not game.move_piece(Position('B8'), Position('C6'))
   assert game.move_piece(Position('G7'), Position('G6'))