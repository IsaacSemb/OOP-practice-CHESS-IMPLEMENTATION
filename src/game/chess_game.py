# src/game/chess_game.py
from typing import Optional, Tuple, List
from src.board.board import Board
from src.game.validation import MoveValidator
from src.pieces.piece import Color, Position, Piece
from src.pieces.concrete_pieces import King, Pawn


class GameState:
    ACTIVE = "ACTIVE"
    CHECKMATE = "CHECKMATE" 
    STALEMATE = "STALEMATE"
    DRAW = "DRAW"


class ChessGame:
    def __init__(self):
        self.board = Board()
        self._current_turn = Color.WHITE
        self._game_state = GameState.ACTIVE
        self._initialize_board()
        
        self.validator = MoveValidator(self.board)

    def _initialize_board(self):
        """Set up initial piece positions"""
        # import all concrete pieces
        from src.pieces.concrete_pieces import (
            Rook,
            Bishop,
            Knight,
            Queen,
            King,
            Pawn
        )
        #  initialize back row pieces
        back_row = [ Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook ]
        files = 'ABCDEFGH'
        
        # white pieces
        for file_idx, piece_class in enumerate(back_row):
            # back row positions
            pos = Position(files[file_idx],1)
            self.board.place_piece(piece_class(Color.WHITE,pos),pos)
            
            # placing pawns
            pawn_pos = Position(files[file_idx],2)
            self.board.place_piece(Pawn(Color.WHITE,pos),pawn_pos)
            
        
        # black pieces
        for file_idx, piece_class in enumerate(back_row):
            # back row positions
            pos = Position(files[file_idx],8)
            self.board.place_piece(piece_class(Color.BLACK,pos),pos)
            
            # placing pawns
            pawn_pos = Position(files[file_idx],7)
            self.board.place_piece(Pawn(Color.BLACK,pos),pawn_pos)


    # def move_piece(self, from_pos: Position, to_pos: Position) -> bool:
    #     """Execute a move if valid"""
    #     if self._game_state != GameState.ACTIVE:
    #         raise GameOverError("Game has ended")
    
    #     piece = self.board.get_piece_at(from_pos)
    #     if not piece or piece.color != self._current_turn:
    #         return False
    
    #     if to_pos not in piece.get_possible_moves(self.board):
    #         return False
    
    #     # Execute move
    #     self.board.move_piece(from_pos, to_pos)
        
    #     # Update game state
    #     self._update_game_state()
    #     self._switch_turn()    
    #    return True
    
    def move_piece(self, from_pos: Position, to_pos: Position) -> bool:
        if self._game_state != GameState.ACTIVE:
            raise GameOverError("Game has ended")
        
        is_valid, error = self.validator.validate_move(from_pos, to_pos)
        if not is_valid:
            return False

        piece = self.board.get_piece_at(from_pos)
        if not piece or piece.color != self._current_turn:
            return False

        if to_pos not in piece.get_possible_moves(self.board):
            return False

        # Handle castling
        if isinstance(piece, King) and abs(ord(to_pos.file) - ord(from_pos.file)) == 2:
            rook_file = 'H' if to_pos.file == 'G' else 'A'
            rook_pos = Position(rook_file, from_pos.rank)
            new_rook_file = 'F' if to_pos.file == 'G' else 'D'
            self.board.move_piece(rook_pos, Position(new_rook_file, from_pos.rank))
        
        # Handle en passant
        if isinstance(piece, Pawn):
            piece.just_moved_two = abs(to_pos.rank - from_pos.rank) == 2
            
            # Capture en passant
            if abs(ord(to_pos.file) - ord(from_pos.file)) == 1 and not self.board.get_piece_at(to_pos):
                captured_pawn_pos = Position(to_pos.file, from_pos.rank)
                self.board.remove_piece(captured_pawn_pos)
                
        # promotion
        # Handle pawn promotion
        if isinstance(piece, Pawn):
            promotion_rank = 8 if piece.color == Color.WHITE else 1
            if to_pos.rank == promotion_rank:
                if not promotion_choice:
                    return False
                # Create new piece of chosen type
                promoted_piece = promotion_choice(piece.color, to_pos)
                self.board.move_piece(from_pos, to_pos)
                self.board.replace_piece(to_pos, promoted_piece)
                return True

        # Execute move
        self.board.move_piece(from_pos, to_pos)
        
        # Update game state
        self._update_game_state()
        self._switch_turn()
        
        return True
    
    def _switch_turn(self):
        """Switch active player"""
        self._current_turn = Color.BLACK if self._current_turn == Color.WHITE else Color.WHITE
    
    def _update_game_state(self):
        """Update game state after each move"""
        if self._is_checkmate():
            self._game_state = GameState.CHECKMATE
        elif self._is_stalemate():
            self._game_state = GameState.STALEMATE
        elif self._is_draw():
            self._game_state = GameState.DRAW



    def _is_checkmate(self) -> bool:
        """
        logic to determine if the current player is ia checkmate state or not
        """
        king = self._find_king(self._current_turn)
        # check for check first
        if not self._is_king_in_check(king):
            return False
        
        current_pieces = self.board.get_pieces_by_color(self._current_turn)
        
        for piece in current_pieces:
            for move in piece. get_possible_moves(self.board):
                if self._does_move_prevent_check(piece, move):
                    return False
        return True


    def _does_move_prevent_check(self, piece:Piece, new_position:Position)->bool:
        """
        test if move prevents check
        """
        # save current state
        old_position = piece.current_position
        
        # just in case moving new piece causes capturing
        # for example to capture the checker
        captured_piece = self.board.get_piece_at(new_position)
        
        
        # try piece in new position
        self.board.move_piece(old_position, new_position)
        
        # check if king is still in check
        king = self._find_king(piece.color)
        still_in_check = self. _is_king_in_check(king)
        
        # restore state
        self.board.move_piece(new_position, old_position)
        if captured_piece:
            self.board.place_piece(captured_piece, new_position)
        
        return not still_in_check
        

    
    def _is_king_in_check(self, king:King):
        """
        check for if current player king is in check or not 
        
        Checks overlapping possible positions of all other pieces 
        """
        opponent_color = Color.BLACK if king.color == Color.WHITE else Color.WHITE
        opponent_pieces = self.board.get_pieces_by_color(opponent_color)
        
        for piece in opponent_pieces:
            if king.current_position in piece.get_possible_moves(self.board):
                return True
        
        return False
        
    def _find_king(self, color:Color):
        """
        find king of a specified color
        """
        pieces = self.board.get_pieces_by_color(color)
        
        for piece in pieces:
            if isinstance(piece, King):
                return piece
        raise RuntimeError(f"No {color} king found on board")
        
    def _is_stalemate(self) -> bool:
        """Determine if current player is in stalemate"""
        king = self._find_king(self._current_turn)
        
        # If king is in check, it's not stalemate
        if self._is_king_in_check(king):
            return False
        
        # Check if any piece has legal moves
        current_pieces = self.board.get_pieces_by_color(self._current_turn)
        
        for piece in current_pieces:
            if piece.get_possible_moves(self.board):
                return False
                
        return True
    
    def _is_draw(self) -> bool:
        """Check for draw conditions"""
        # Insufficient material
        pieces = self.board.get_pieces_by_color(Color.WHITE) + self.board.get_pieces_by_color(Color.BLACK)
        
        if len(pieces) == 2:  # Only kings remaining
            return True
                
        
        #  shall add other draw conditions like threefold repetition and fifty-move rule.
        return False

class GameOverError(Exception):
    pass