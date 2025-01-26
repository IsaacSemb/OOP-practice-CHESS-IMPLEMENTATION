# src/game/validation.py
from typing import Optional
from src.pieces.piece import Piece, PieceType, Position, Color
from src.board.board import Board

class MoveValidator:
    def __init__(self, board: Board):
        self.board = board

    def validate_move(self, from_pos: Position, to_pos: Position) -> tuple[bool, Optional[str]]:
        piece = self.board.get_piece_at(from_pos)
        
        if not piece:
            return False, "No piece at source position"
            
        if to_pos not in piece.get_possible_moves(self.board):
            return False, "Invalid move for this piece"
            
        # Simulate move to check if it exposes king
        if self._does_move_expose_king(piece, from_pos, to_pos):
            return False, "Move would put/leave king in check"
            
        return True, None
        
    def _does_move_expose_king(self, piece: Piece, from_pos: Position, to_pos: Position) -> bool:
        # Save board state
        captured_piece = self.board.get_piece_at(to_pos)
        
        # Execute move
        self.board.move_piece(from_pos, to_pos)
        
        # Check if king is in check
        king_in_check = self._is_king_in_check(piece.color)
        
        # Restore board state
        self.board.move_piece(to_pos, from_pos)
        if captured_piece:
            self.board.place_piece(captured_piece, to_pos)
            
        return king_in_check

    def _is_king_in_check(self, color: Color) -> bool:
        king_pos = self._find_king_position(color)
        opponent_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        
        for pos, piece in self.board.get_all_pieces():
            if piece and piece.color == opponent_color:
                if king_pos in piece.get_possible_moves(self.board):
                    return True
        return False
        
    def _find_king_position(self, color: Color) -> Position:
        for pos, piece in self.board.get_all_pieces():
            if piece and piece.color == color and piece.piece_type == PieceType.KING:
                return pos
        raise ValueError(f"No {color} king found")