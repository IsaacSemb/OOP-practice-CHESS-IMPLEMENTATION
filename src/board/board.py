from typing import Dict, Optional
from src.pieces.piece import  Piece, Position, Color

class Board:
    def __init__(self):
        """
        Create an empty chess board with a sophisticated representation
        
        Design Considerations:
        - Immutable board state
        - Efficient piece lookup
        - Clear spatial relationships
        """
        self._board_state: Dict[Position, Optional[Piece]] = {}
        self._initialize_empty_board()
    
    # internal method start with underscore
    def _initialize_empty_board(self):
        """
        Systematically create board positions
        
        Demonstrates:
        - Comprehensive initialization
        - Explicit position creation
        """
        
        # get rows and columns
        files = 'ABCDEFGH'
        ranks = range(1,9)
        
        # create the files 
        for file in files:
            # for every file lay out all the ranks
            for rank in ranks:
                position = Position(file, rank)
                self._board_state[position] = None
    
    def place_piece(self, piece:Piece, position:Position):
        """
        Place a piece on the board with validation
        
        OOP Principles:
        - Encapsulation of board state
        - Explicit state modification rules
        """
        
        if position not in self._board_state:
            raise ValueError(f" Invalid board position {position}")
        
        if self._board_state[position] is not None:
            raise ValueError(f"Position {position} is already occupied")
    
    def move_piece (self, from_position:Position, to_position:Position):
        """
        Execute a piece move with comprehensive checks
        
        Key Responsibilities:
        - Validate move legality
        - Update board state
        - Handle piece captures
        """
        
        # pick up piece to move
        moving_piece = self.get_piece_at(from_position)
        
        # if its an empty spot
        if moving_piece is None:
            raise ValueError(f'No piece at {from_position}')  
        
        # incase there is a piece there already for capture
        captured_piece = self.get_piece_at(to_position)
        
        # update the board state
        self._board_state[to_position] =  moving_piece
        self._board_state[from_position] = None
        
        return captured_piece
    
    def get_piece_at(self, position:Position)-> Optional[Piece]:
        """
        Retrieve piece at a specific position
        
        Design Patterns:
        - Provides controlled access to board state
        - Prevents direct manipulation of the board by encapsulating it in this function
        """
        return self._board_state.get(position)
    
    def is_move_valid(self, piece:Piece, destination:Position)-> bool:
        """
        Preliminary move validation
        
        This will be a collaborative method between:
        - Piece-specific movement rules
        - Board-level constraints
        """
        # Initial basic checks
        # Will be dramatically expanded in future iterations
        return destination in piece.get_possible_moves(self)
    
    def get_pieces_by_color(self, color:Color) -> list[Piece]:
        """
        Retrieve all pieces of a specific color
        
        Demonstrates:
        - Complex querying
        - State exploration
        """
        
        # comprehension
        return [
            piece for piece in self._board_state.values()
            if piece is not None and piece.color == color
        ]
    
    def __str__(self):
        """
        Create a string representation of the board
        
        OOP Principle:
        - Provide meaningful object representation
        """
        board_view = []
        for rank in range(8, 0, -1):
            rank_view = []
            for file in 'ABCDEFGH':
                position = Position(file, rank)
                piece = self.get_piece_at(position)
                rank_view.append(piece.__class__.__name__[0] if piece else '.')
            board_view.append(' '.join(rank_view))
        return '\n'.join(board_view)