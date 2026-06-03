import pytest
import inspect

# Import your file as an alias (change 'graph_search' to your actual filename)
import graph_problems.depth_first_search as target_file

# --- 1. Structural Tests ---

def test_dfs_function_exists():
    """User Story 1: You should have a function named dfs that takes two arguments."""
    assert hasattr(target_file, "dfs"), "Function must be named 'dfs'"
    
    sig = inspect.signature(target_file.dfs)
    assert len(sig.parameters) == 2, "The dfs function must accept exactly two arguments (matrix, start_node)."


# --- 2. Lab Required Exact Match Tests ---

@pytest.mark.parametrize("matrix, start_node, expected_nodes", [
    # User Story 2 & 3: A standard 4-node line graph
    ([[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]], 1, [1, 2, 3, 0]),
    ([[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]], 3, [1, 2, 3, 0]),
    
    # User Story 4: An isolated node (Node 3 is disconnected)
    ([[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]], 3, [3]),
    
    # User Story 5 & 6: A graph split into two disconnected pairs (0-1 and 2-3)
    ([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], 3, [3, 2]),
    ([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], 0, [0, 1]),
])
def test_lab_required_cases(matrix, start_node, expected_nodes):
    """Tests the exact matrix inputs requested by the lab grading table."""
    result = target_file.dfs(matrix, start_node)
    
    # We use sets so the test passes regardless of the specific traversal order
    assert set(result) == set(expected_nodes), f"Failed starting at node {start_node}"


# --- 3. Edge Cases ---

def test_single_node_graph():
    """Edge Case: The smallest possible valid graph (1 node)."""
    matrix = [[0]]
    assert target_file.dfs(matrix, 0) == [0]

def test_fully_connected_graph():
    """Edge Case: Every node connects to every other node."""
    matrix = [
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0]
    ]
    result = target_file.dfs(matrix, 0)
    assert set(result) == {0, 1, 2}