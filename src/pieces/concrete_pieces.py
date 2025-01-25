
from src.pieces.piece import Color, Piece, PieceType, Position
from src.pieces.movement import MovementStrategyFactory


class Rook(Piece):
    def __init__(self, color:Color, position:Position):
        super().__init__(color, position)
        self.movement_strategy = MovementStrategyFactory.get_movement_strategy(Rook)
    
    def get_possible_moves(self, board):
        return self.movement_strategy.calculate_possible_moves(self, board)
    
    @property
    def piece_type(self) -> PieceType:
        return PieceType.ROOK


class Knight(Piece):
    def __init__(self, color:Color, position:Position):
        super().__init__(color, position)
        self.movement_strategy = MovementStrategyFactory.get_movement_strategy(Rook)

    def get_possible_moves(self, board):
        return self.movement_strategy.calculate_possible_moves(self, board)
    
    @property
    def piece_type(self) -> PieceType:
        return PieceType.KNIGHT



class Bishop(Piece):
    def __init__(self, color:Color, position:Position):
        super().__init__(color, position)
        self.movement_strategy = MovementStrategyFactory.get_movement_strategy(Rook)

    def get_possible_moves(self, board):
        return self.movement_strategy.calculate_possible_moves(self, board)
    
    @property
    def piece_type(self) -> PieceType:
        return PieceType.BISHOP



class Queen(Piece):
    def __init__(self, color:Color, position:Position):
        super().__init__(color, position)
        self.movement_strategy = MovementStrategyFactory.get_movement_strategy(Rook)

    def get_possible_moves(self, board):
        return self.movement_strategy.calculate_possible_moves(self, board)
    
    @property
    def piece_type(self) -> PieceType:
        return PieceType.QUEEN



class King(Piece):
    def __init__(self, color:Color, position:Position):
        super().__init__(color, position)
        self.movement_strategy = MovementStrategyFactory.get_movement_strategy(Rook)

    def get_possible_moves(self, board):
        return self.movement_strategy.calculate_possible_moves(self, board)
    
    @property
    def piece_type(self) -> PieceType:
        return PieceType.KING



class Pawn(Piece):
    def __init__(self, color:Color, position:Position):
        super().__init__(color, position)
        self.movement_strategy = MovementStrategyFactory.get_movement_strategy(Rook)

    def get_possible_moves(self, board):
        return self.movement_strategy.calculate_possible_moves(self, board)
    
    @property
    def piece_type(self) -> PieceType:
        return PieceType.PAWN


