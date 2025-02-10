import sys
import os
# Add the root directory to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(root_path) 


import pytest
from src.pieces.piece import Position



# testing the position class

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

