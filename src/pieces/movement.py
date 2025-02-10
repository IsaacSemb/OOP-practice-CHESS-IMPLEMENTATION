from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Type
from src.board.board import Board
from src.game.moves import PromotionMove
from src.pieces.piece import Position, Piece, Color


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
        
        from src.pieces.concrete_pieces import ( Rook, Knight, Queen, Bishop )
        
        possible_moves = []
        current_pos = piece.current_position
        promotion_rank = 8 if piece.color == Color.WHITE else 1
        
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
            
        for move in possible_moves:
            if move.rank == promotion_rank:
                # Add promotion moves for each possible piece type
                for promotion_type in [Queen, Rook, Bishop, Knight]:
                    possible_moves.append(PromotionMove(move, promotion_type))
            else:
                possible_moves.append(move)
                    
        # Add en passant moves
        possible_moves.extend(self._get_en_passant_moves(piece, board))
            
        return possible_moves
    
    def _get_en_passant_moves(self, piece: Piece, board: Board) -> List[Position]:
        if piece.current_position.rank != (5 if piece.color == Color.WHITE else 4):
            return []
            
        en_passant_moves = []
        for direction in [-1, 1]:
            try:
                adjacent_file = chr(ord(piece.current_position.file) + direction)
                adjacent_pos = Position(adjacent_file, piece.current_position.rank)
                
                adjacent_piece = board.get_piece_at(adjacent_pos)
                if (isinstance(adjacent_piece) and 
                    adjacent_piece.color != piece.color and 
                    adjacent_piece.just_moved_two):
                    
                    capture_rank = piece.current_position.rank + (1 if piece.color == Color.WHITE else -1)
                    en_passant_moves.append(Position(adjacent_file, capture_rank))
            except ValueError:
                continue
                
        return en_passant_moves



class KingMovementStrategy(MovementStrategy):
    def calculate_possible_moves(self, piece, board:Board):
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
        
        # Add castling moves if conditions are met
        if not piece.has_moved and not self._is_king_in_check(piece, board):
            # Kingside castling
            kingside_rook = self._get_rook_for_castling(piece, board, 'H')
            if kingside_rook and self._can_castle_kingside(piece, kingside_rook, board):
                possible_moves.append(Position('G', piece.current_position.rank))
                
            # Queenside castling
            queenside_rook = self._get_rook_for_castling(piece, board, 'A')
            if queenside_rook and self._can_castle_queenside(piece, queenside_rook, board):
                possible_moves.append(Position('C', piece.current_position.rank))
                
            
        return possible_moves

    def _get_rook_for_castling(self, king: Piece, board: Board, file: str) -> Optional[Piece]:
        rook_pos = Position(file, king.current_position.rank)
        rook = board.get_piece_at(rook_pos)
        return rook if isinstance(rook) and not rook.has_moved else None

    def _can_castle_kingside(self, king: Piece, rook: Piece, board: Board) -> bool:
        return self._is_path_clear(king, rook, board, ['F', 'G'])

    def _can_castle_queenside(self, king: Piece, rook: Piece, board: Board) -> bool:
        return self._is_path_clear(king, rook, board, ['B', 'C', 'D'])

    def _is_path_clear(self, king: Piece, rook: Piece, board: Board, files: List[str]) -> bool:
        rank = king.current_position.rank
        return all(
            not board.get_piece_at(Position(file, rank)) and 
            not self._is_square_attacked(Position(file, rank), board, king.color)
            for file in files
        )




class MovementStrategyFactory:
    """
    Centralized strategy selection for piece movement
    
    Design Patterns:
    - Factory Method
    - Strategy Pattern
    """
    from src.pieces.concrete_pieces import ( Rook, Knight, Bishop, Queen, King, Pawn )
    
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