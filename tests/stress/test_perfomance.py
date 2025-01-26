# tests/stress/test_performance.py
import time
import pytest
from src.board.board import Board
from src.game.chess_game import ChessGame
from src.pieces.concrete_pieces import Bishop, King, Knight, Queen, Rook
from src.pieces.piece import Color, Position

def test_complex_position_calculation():
    game = ChessGame()
    # Set up complex middle-game position with many possible moves
    setup_moves = [
        ('E2', 'E4'), ('E7', 'E5'),
        ('G1', 'F3'), ('B8', 'C6'),
        ('F1', 'B5'), ('G8', 'F6'),
        ('D2', 'D3'), ('F8', 'C5'),
    ]
    for from_pos, to_pos in setup_moves:
        game.move_piece(Position(*from_pos), Position(*to_pos))
    
    start_time = time.time()
    # Calculate all possible moves for all pieces
    for pos, piece in game.board.get_all_pieces():
        if piece:
            piece.get_possible_moves(game.board)
    end_time = time.time()
    
    assert (end_time - start_time) < 1.0  # Should complete within 1 second
    
# tests/stress/test_performance.py

def test_massive_move_calculation():
   """Test calculating all possible moves in a crowded board"""
   game = ChessGame()
   moves = 0
   start_time = time.time()
   
   # Calculate moves for 20 turns
   for _ in range(20):
       for pos, piece in game.board.get_all_pieces():
           if piece:
               moves += len(piece.get_possible_moves(game.board))
   
   duration = time.time() - start_time
   assert duration < 2.0
   assert moves > 1000

def test_check_detection_performance():
   """Test check detection with many threatening pieces"""
   board = Board()
   king = King(Color.WHITE, Position('E', 4))
   board.place_piece(king, Position('E', 4))
   
   # Add multiple threatening pieces
   enemy_pieces = [
       (Queen, 'D', 8),
       (Rook, 'E', 8), 
       (Rook, 'H', 4),
       (Bishop, 'H', 7),
       (Knight, 'F', 6)
   ]
   
   for piece_type, file, rank in enemy_pieces:
       board.place_piece(piece_type(Color.BLACK, Position(file, rank)), 
                        Position(file, rank))
   
   start_time = time.time()
   # Run check detection multiple times
   for _ in range(1000):
       king.get_possible_moves(board)
   
   assert time.time() - start_time < 1.0

def test_consecutive_game_creation():
   """Test creating and initializing multiple games"""
   start_time = time.time()
   games = []
   
   for _ in range(100):
       game = ChessGame()
       games.append(game)
       
   assert time.time() - start_time < 1.0
   assert len(games) == 100

def test_rapid_move_execution():
   """Test executing many moves rapidly"""
   game = ChessGame()
   moves = [
       ('E2', 'E4'), ('E7', 'E5'),
       ('G1', 'F3'), ('B8', 'C6'),
       ('F1', 'B5'), ('A7', 'A6')
   ]
   
   start_time = time.time()
   for _ in range(100):
       for from_pos, to_pos in moves:
           game.move_piece(Position(*from_pos), Position(*to_pos))
           
   assert time.time() - start_time < 2.0