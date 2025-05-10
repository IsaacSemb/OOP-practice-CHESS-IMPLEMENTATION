import sys
import os

# Add the root directory to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(root_path) 


import pytest
from src.pieces.piece import Color, PieceType, Position



def test_color_enum():
    """
    Test the Color enum values.
    """
    assert Color.BLACK.value == "BLACK"
    assert Color.WHITE.value == "WHITE"

    
def test_color_enum_names():
    """
    Test the Color enum names.
    """
    assert Color.WHITE.name == "WHITE"
    assert Color.BLACK.name == "BLACK"

def test_piece_names():
    """
    validate the names types of pieces
    """
    assert PieceType.KING.name == "KING"
    assert PieceType.QUEEN.name == "QUEEN"
    assert PieceType.KNIGHT.name == "KNIGHT"
    assert PieceType.BISHOP.name == "BISHOP"
    assert PieceType.ROOK.name == "ROOK"
    assert PieceType.PAWN.name == "PAWN"



def test_valid_position():
    position = Position("A", 1)
    assert str(position) == "A1"
    assert repr(position) == "Position(A, 1)"
    

# use of lowercase letter to instantiate the position class
def test_valid_position_lowercase():
    position = Position("d", 1)
    assert str(position) == "D1"
    assert repr(position) == "Position(D, 1)"


def test_invalid_position_out_of_bounds():
    with pytest.raises(ValueError):
        Position("I", 1)  # invalid file
    with pytest.raises(ValueError):
        Position("A", 9)  # invalid rank
        
def test_invalid_position_wrong_data_type():
    with pytest.raises(TypeError):
        Position("A", "e")  # invalid rank
    with pytest.raises(TypeError):
        Position(1, "e")  # invalid rank

