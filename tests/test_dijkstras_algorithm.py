import pytest

# Assuming your code is saved in a file called dijkstra.py
from graph_problems.dijkstra_algorithm import shortest_path

INF = float('inf')

# The graph provided in your example
STANDARD_MATRIX = [
    [0, 5, 3, INF, 11, INF],
    [5, 0, 1, INF, INF, 2],
    [3, 1, 0, 1, 5, INF],
    [INF, INF, 1, 0, 9, 3],
    [11, INF, 5, 9, 0, INF],
    [INF, 2, INF, 3, INF, 0],
]

def test_shortest_path_standard():
    """Tests the standard path from 0 to 5 using the provided matrix."""
    distances, paths = shortest_path(STANDARD_MATRIX, 0, 5)
    
    # The true shortest distance is 6 via nodes 0 -> 2 -> 1 -> 5
    assert distances[5] == 6
    assert paths[5] == [0, 2, 1, 5]

def test_shortest_path_all_nodes():
    """Tests if all distances are calculated correctly when target is None."""
    distances, paths = shortest_path(STANDARD_MATRIX, 0)
    
    # The true shortest distances to all nodes [0, 1, 2, 3, 4, 5]
    expected_distances = [0, 4, 3, 4, 8, 6]
    assert distances == expected_distances
    
    # Check a specific path, e.g., to node 4
    assert paths[4] == [0, 2, 4]

# --- Edge Cases ---

def test_start_node_to_itself():
    """Edge Case: The target node is the same as the start node."""
    distances, paths = shortest_path(STANDARD_MATRIX, 2, 2)
    
    assert distances[2] == 0
    assert paths[2] == [2]

def test_unreachable_node():
    """Edge Case: A graph where a node is completely isolated."""
    isolated_matrix = [
        [0, 5, INF],
        [5, 0, INF],
        [INF, INF, 0] # Node 2 is isolated
    ]
    distances, paths = shortest_path(isolated_matrix, 0)
    
    # Distance to node 2 should remain infinity
    assert distances[2] == INF
    assert distances[1] == 5

def test_single_node_graph():
    """Edge Case: The smallest possible valid graph (1 node)."""
    single_node_matrix = [[0]]
    distances, paths = shortest_path(single_node_matrix, 0)
    
    assert distances == [0]
    assert paths == [[0]]