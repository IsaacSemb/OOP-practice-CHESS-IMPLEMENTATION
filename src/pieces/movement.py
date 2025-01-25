from abc import ABC, abstractmethod
from typing import Dict, List, Type
from src.board.board import Board
from src.pieces.piece import Position, Piece, Color
from src.pieces.concrete_pieces import (
    Rook,
    Knight,
    Bishop,
    Queen,
    King,
    Pawn 
    )

class MovementStrategy(ABC):
    
    @abstractmethod
    def calculate_possible_moves(self, piece:Piece, board:Board)->List[Position]:
        """
        Core movement calculation strategy
        
        Args:
            piece: The piece being moved
            board: Current board state
        
        Returns:
            List of valid destination positions
        """
        pass

class RookMovementStrategy(MovementStrategy):
    def calculate_possible_moves(self, piece, board)-> List[Position]:
        """
        Rook movement logic:
        - Moves horizontally and vertically
        - Stops at board edges or blocked squares
        - Can capture opponent pieces
        """
        possible_moves = []
        current_pos = piece.current_position
        
        directions = [
            (0, 1), # North
            (0, -1), # South
            (1, 0), # East
            (-1, 0), # West
        ]
        
        # unpack the directions into verrtical and horizontal 
        for dx, dy in directions:
            
            for step in range(1,8): # the most it can go is 7 from the starting line
                # get current position letter convert it to number, add the steps you moved, convert the wwhole thing back to character  
                new_file = chr(ord(current_pos.file) + dx*step)
                new_rank = current_pos.rank + dy*step
                
                # validation of the new position
                try:
                    new_pos = Position(new_file,new_rank)
                except ValueError:
                    # it means youre outside the board
                    break
                
                # incase when moving there is a blocking piece (we check whether we are sure or not)
                blocking_piece = board.get_piece_at(new_pos)
                
                if blocking_piece:
                    
                    # if its our team or opponent
                    if blocking_piece.color != piece.color:
                        possible_moves.append(new_pos)
                    break
                
                possible_moves.append(new_pos)
        
        return possible_moves
    
    
    
class KnightMovementStrategy(MovementStrategy):
    def calculate_possible_moves( self, piece: Piece, board: Board ) -> List[Position]:
        """
        Knight movement logic:
        - L-shaped movement
        - Can jump over other pieces
        """
        possible_moves = []
        current_pos = piece.current_position

        # 8 L-shaped possible formats
        knight_moves = [ (1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1) ]

        for dx, dy in knight_moves:
            new_file = chr(ord(current_pos.file) + dx)
            new_rank = current_pos.rank + dy

            # Validate and process potential move
            try:
                new_pos = Position(new_file, new_rank)
                blocking_piece = board.get_piece_at(new_pos)

                # Can move to empty squares or capture opponent pieces
                if not blocking_piece or blocking_piece.color != piece.color:
                    possible_moves.append(new_pos)
            except ValueError:
                # Invalid board position, skip
                continue

        return possible_moves


class BishopMovementStrategy(MovementStrategy):
    def calculate_possible_moves(self, piece:Piece, board:Board):
        
        possible_moves = []
        current_pos = piece.current_position
        
        # setting out diagonal moves for ther bishop
        directions = [
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1)
        ]
        
        for dx, dy in directions:
            for step in range(1,8):
                new_file = chr(ord(current_pos.file) + dx*step)
                new_rank = current_pos.rank +dy*step
                
                try:
                    new_pos = Position(new_rank, new_file)
                except ValueError:
                    break
                
                # incase of blocking piece
                blocking_piece = board.get_piece_at(new_pos)
                
                # incase there is a blocking piece
                if blocking_piece:
                    if blocking_piece.color != piece.color:
                        possible_moves.append(new_pos)
                
                possible_moves.append(new_pos)
        
        return possible_moves



class QueenMovementStrategy(MovementStrategy):
    def __init__(self):
        self.rook_strategy = RookMovementStrategy()
        self.bishop_strategy = BishopMovementStrategy()

    def calculate_possible_moves(self, piece:Piece, board:Board)->List[Position]:
        rook_moves = self.rook_strategy.calculate_possible_moves(piece,board)
        bishop_moves = self.bishop_strategy.calculate_possible_moves(piece,board)
        return rook_moves + bishop_moves

class PawnMovementStrategy(MovementStrategy):
    def calculate_possible_moves(self, piece:Piece, board:Board):
        possible_moves = []
        current_pos = piece.current_position
        
        # separate light player and dark player sense of direction
        direction = 1 if piece.color == Color.WHITE else -1
        
        # movement logic
        new_rank = current_pos.rank + direction
                
        try:
            # validate the movement
            forward_pos = Position(current_pos.file, new_rank)
            
            # check for obstacles
            if not board.get_piece_at(forward_pos):
                possible_moves.append(forward_pos)
            
            
            # double moving at the beginning
            if not piece.has_moved:
                double_rank = current_pos.rank + (2*direction)
                double_pos = Position(current_pos.file, double_rank)
                
                # check if obstacle
                if not board. get_piece_at(double_pos):
                    possible_moves.append(double_pos)
                    
        except ValueError:
            pass
        
        # capturing logic
        for dx in [-1, 1]:
            try:
                new_file = chr(ord(current_pos.file) + dx)
                capture_pos = Position(new_file, new_rank)
                target = board.get_piece_at(capture_pos)
                
                if target and target.color != piece.color:
                    possible_moves.append(capture_pos)
            except ValueError:
                continue
            
        return possible_moves



class KingMovementStrategy(MovementStrategy):
    def calculate_possible_moves(self, piece:Piece, board:Board):
        possible_moves = []
        current_pos = piece.current_position
        
        # all adjacent position 
        directions = [ (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1),  (1, 0),  (1, 1) ]
    
        for dx, dy in directions:
            new_file = chr(ord(current_pos.file) + dx)
            new_rank = current_pos.rank + dy
            
            # validate the new position
            try:
                new_pos = Position(new_file, new_rank)
                
                # incase of any blockers
                blocking_piece = board.get_piece_at(new_pos)
                
                if not blocking_piece or blocking_piece.color != piece.color:
                    possible_moves.append(new_pos)
            
            except ValueError:
                continue
            
        return possible_moves





class MovementStrategyFactory:
    """
    Centralized strategy selection for piece movement
    
    Design Patterns:
    - Factory Method
    - Strategy Pattern
    """
    _strategies: Dict[Type[Piece], Type[MovementStrategy]] = {
        Rook: RookMovementStrategy,
        Knight: KnightMovementStrategy,
        Bishop: BishopMovementStrategy,
        Queen: QueenMovementStrategy,
        King: KingMovementStrategy,
        Pawn: PawnMovementStrategy,        
    }

    @classmethod
    def get_movement_strategy( cls, piece_type: Type[Piece] ) -> MovementStrategy:
        """
        Dynamically select appropriate movement strategy
        
        Demonstrates:
        - Runtime strategy selection
        - Extensible design
        """
        strategy_class = cls._strategies.get(piece_type)
        if not strategy_class:
            raise ValueError(f"No movement strategy for {piece_type}")
        
        return strategy_class()