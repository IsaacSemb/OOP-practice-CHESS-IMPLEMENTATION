# src/game/moves.py
from typing import Type
from src.pieces.piece import Piece, Position

class PromotionMove:
    def __init__(self, position: Position, promotion_piece_type: Type[Piece]):
        self.position = position
        self.promotion_piece_type = promotion_piece_type
        
    def __eq__(self, other):
        if isinstance(other, Position):
            return other == self.position
        return isinstance(other, PromotionMove) and other.position == self.position
        
    def __hash__(self):
        return hash(self.position)