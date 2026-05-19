import pytest
from abc import ABC
import inspect
import random
from abstraction.player_interface import Player, Pawn  # Adjust 'game' if your filename is different


# =====================================================================
# 1. STRUCTURAL AND REFACTORING TESTS (User Story Compliance)
# =====================================================================

def test_player_is_abstract_class():
    """Ensure Player inherits from ABC and cannot be instantiated directly."""
    assert issubclass(Player, ABC)
    with pytest.raises(TypeError):
        Player()


def test_player_init_parameters():
    """Edge Case/Strict Test: Ensure Player.__init__ accepts ONLY 'self'."""
    sig = inspect.signature(Player.__init__)
    assert len(sig.parameters) == 1
    assert "self" in sig.parameters


def test_player_make_move_parameters():
    """Edge Case/Strict Test: Ensure make_move accepts ONLY 'self'."""
    sig = inspect.signature(Player.make_move)
    assert len(sig.parameters) == 1
    assert "self" in sig.parameters


# =====================================================================
# 2. PAWN INITIALIZATION TESTS
# =====================================================================

def test_pawn_initial_state():
    """Verify that a newly instantiated Pawn has the correct initial state."""
    pawn = Pawn()
    assert pawn.position == (0, 0)
    assert pawn.path == [(0, 0)]
    
    # Check that it has exactly the 4 standard directional moves
    expected_initial_moves = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    assert len(pawn.moves) == 4
    for move in expected_initial_moves:
        assert move in pawn.moves


# =====================================================================
# 3. MOVEMENT LOGIC & EDGE CASES
# =====================================================================

def test_pawn_make_move_updates_state():
    """Verify that making a move correctly changes position, path, and returns new position."""
    pawn = Pawn()
    
    # Mock random.choice to guarantee a deterministic outcome for testing
    # Force it to choose 'Up' (0, 1)
    random.choice = lambda x: (0, 1)
    
    new_pos = pawn.make_move()
    
    assert new_pos == (0, 1)
    assert pawn.position == (0, 1)
    assert pawn.path == [(0, 0), (0, 1)]


def test_edge_case_movement_canceling_out():
    """
    Edge Case: Verify path accumulation and position tracking when consecutive 
    moves cancel each other out dynamically (returning to origin).
    """
    pawn = Pawn()
    
    # Move Up
    random.choice = lambda x: (0, 1)
    pawn.make_move()
    
    # Move Down (cancels out up)
    random.choice = lambda x: (0, -1)
    pawn.make_move()
    
    assert pawn.position == (0, 0)  # Back at origin
    assert len(pawn.path) == 3      # Starting point + 2 movements tracked
    assert pawn.path == [(0, 0), (0, 1), (0, 0)]


def test_edge_case_randomness_distribution():
    """
    Edge Case: Ensure make_move actively samples from all available options.
    If we run it 100 times, it shouldn't just pick the same move over and over.
    """
    # Restore the real random.choice implementation for this test
    import importlib
    importlib.reload(random)
    
    pawn = Pawn()
    positions_visited = set()
    
    for _ in range(50):
        pawn.make_move()
        positions_visited.add(pawn.position)
        
    # If random.choice is working natively, a pawn moving 50 times 
    # will sample varied routes and visit multiple distinct grid spaces.
    assert len(positions_visited) > 1 


# =====================================================================
# 4. LEVEL UP LOGIC & EDGE CASES
# =====================================================================

def test_pawn_level_up_adds_diagonals():
    """Verify that leveling up expands moves from 4 to 8, including all diagonals."""
    pawn = Pawn()
    pawn.level_up()
    
    expected_all_moves = [
        (0, 1), (0, -1), (-1, 0), (1, 0),      # Standard
        (1, 1), (1, -1), (-1, -1), (-1, 1)     # Diagonals
    ]
    
    assert len(pawn.moves) == 8
    for move in expected_all_moves:
        assert move in pawn.moves


def test_edge_case_multiple_level_ups():
    """
    Edge Case: What happens if level_up() is called multiple times?
    Ensure it doesn't break movement loops, but tracks added moves correctly.
    """
    pawn = Pawn()
    pawn.level_up()
    pawn.level_up()  # Second call
    
    # It will append them again, meaning total moves becomes 12
    assert len(pawn.moves) == 12
    
    # Ensure movement logic still processes flawlessly with a larger list pool
    random.choice = lambda x: x[-1]  # Force select the last diagonal added (-1, 1)
    new_pos = pawn.make_move()
    assert new_pos == (-1, 1)