from abc import ABC, abstractmethod
from enum import Enum, auto


class Color(Enum):
    """
    Enumeration of the piece colors  
    In chess, pieces are either `black` or `white`, 
    this enum is used to represent the two colors.  
    """
    WHITE = "WHITE"
    BLACK = "BLACK"


class PieceType(Enum):
    """
    Enumeration of the piece types
    We have 6 types of pieces in chess:
    - Pawn
    - Rook
    - Knight
    - Bishop
    - Queen
    - King  
    Each piece type is represented as an enum member  
    """
    PAWN = "PAWN"
    ROOK = "ROOK"
    KNIGHT = "KNIGHT"
    BISHOP = "BISHOP"
    QUEEN = "QUEEN"
    KING = "KING"


class Position:
    def __init__(self, file:str, rank:int):
        """
        Validates and stores chess board position
        
        Args:
            file (str): Column letter (A-H)
            rank (int): Row number (1-8)
        """
        
        # checking for file(row) and rank(column) -- this basically self validates
        if not ( 1<=rank<=8 and file.upper() in 'ABCDEFGH' ):
            raise ValueError(f"Invalid chess position {file}{rank}")
        
        # if the file and rank are valid then assign them
        self.file = file.upper()
        self.rank = rank
    
    def __str__(self):
        """
        a string representation of the class instance
        """
        return f"{self.file}{self.rank}"
    
    def __repr__(self):
        """
        Returns a string representation of the piece's position.
        The string is formatted as 'Position(file, rank)', where `file` and `rank`
        represent the piece's current position on the chessboard.
        Returns:
            str: A string representation of the piece's position.
        """
        return f"Position({self.file}, {self.rank})"


class Piece(ABC):
    def __init__(self, color:Color, initial_position:Position):
        """
        Base Class for all the chess pieces
        
        Args:
            color (Color): Piece color
            initial_position (Position): Starting board position
        """
        self._color = color
        self._current_position = initial_position
        self._has_moved = False
        self.just_moved_two = False  # For en passant tracking
        
    @property
    def color(self) -> Color:
        """
        getter for the color of a piece
        """
        return self._color
    
    @property
    def current_position(self) -> Position:
        """
        getter of current piece position
        """
        return self._current_position

    @property
    def has_moved(self) -> bool:
        """
        Track if piece has been moved
        """
        return self._has_moved

    def move(self, new_position: Position):
        """
        Move piece to a new position
        
        Args:
            new_position (Position): Destination position
        """
        if self._is_move_valid(new_position):
            self._current_position = new_position
            self._has_moved = True
        else:
            raise ValueError(f"Invalid move for {self.__class__.__name__} to {new_position}")
    
    @abstractmethod
    def _is_move_valid(self, new_position:Position) -> bool:
        """
        Abstract method to validate piece-specific move rules
        
        Args:
            new_position (Position): Proposed move destination
        
        Returns:
            bool: Whether the move is valid
        """
        pass
    
    @abstractmethod
    def get_possible_moves(self,board) -> list[Position]:
        """
        Calculate all possible moves for this piece
        
        Args:
            board: Current board state
        
        Returns:
            list[Position]: All valid move positions
        """
        pass
    
    @property
    @abstractmethod
    def piece_type(self) -> PieceType:
        """
        defines the speecific piece type
        
        Returns:
        PieceType: Enum representing piece type
        """
        pass
