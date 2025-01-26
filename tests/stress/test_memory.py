# tests/stress/test_memory.py
import psutil
import gc
import pytest
from src.game.chess_game import ChessGame
from src.pieces.piece import Position

def get_memory_usage():
   """Get current memory usage in MB"""
   process = psutil.Process()
   return process.memory_info().rss / (1024 * 1024)

def test_memory_leak_multiple_games():
   initial_memory = get_memory_usage()
   games = []
   
   for _ in range(1000):
       games.append(ChessGame())
   
   del games
   gc.collect()
   
   final_memory = get_memory_usage()
   memory_diff = final_memory - initial_memory
   
   assert memory_diff < 10  # Less than 10MB difference

def test_memory_long_game():
   game = ChessGame()
   initial_memory = get_memory_usage()
   
   # Play 50 moves
   moves = [
       ('E2', 'E4'), ('E7', 'E5'),
       ('G1', 'F3'), ('B8', 'C6')
   ] * 25
   
   for from_pos, to_pos in moves:
       game.move_piece(Position(*from_pos), Position(*to_pos))
   
   final_memory = get_memory_usage()
   assert final_memory - initial_memory < 5  # Less than 5MB growth

def test_memory_board_states():
   initial_memory = get_memory_usage()
   boards = []
   
   for _ in range(500):
       game = ChessGame()
       boards.append(game.board)
       
   current_memory = get_memory_usage()
   del boards
   gc.collect()
   
   final_memory = get_memory_usage()
   assert final_memory - initial_memory < 2  # Memory properly freed