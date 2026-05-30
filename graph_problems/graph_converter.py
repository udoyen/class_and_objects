def adjacency_list_to_matrix(adj_list):
    """Converts an adjacency list to an adjacency matrix."""
    # User Story 1: Determine the number of nodes
    num_nodes = len(adj_list)
    
    # User Story 2: Initialize a square matrix of size num_nodes x num_nodes with zeros
    matrix = [[0 for _ in range(num_nodes)] for _ in range(num_nodes)]
    
    # User Story 3: Fill the matrix based on the adjacency list
    for node, neighbors in adj_list.items(): # node is the index, neighbors are the connected nodes
        for neighbor in neighbors: # Set the corresponding entry in the matrix to 1 for each edge
            matrix[node][neighbor] = 1
    
    # User Story 4: Print each row of the matrix
    for row in matrix:
        print(row)
    
    # User Story 5: Return the adjacency matrix
    return matrix



def adjacency_matrix_to_list(adj_matrix):
    """Converts an adjacency matrix to an adjacency list."""
    adj_list = {} # Initialize an empty dictionary to hold the adjacency list
    for i in range(len(adj_matrix)): # Iterate through each row of the matrix
        adj_list[i] = [] # Initialize the list for the current node
        for j in range(len(adj_matrix[i])): # Iterate through each column in the current row
            if adj_matrix[i][j] == 1: # If there's an edge (indicated by a 1), add the neighbor to the list
                adj_list[i].append(j)
    return adj_list

if __name__ == "__main__": # pragma: no cover
    # Example usage
    adj_list = {0: [1, 2], 1: [2], 2: [0, 3], 3: [2]}
    adjacency_list_to_matrix(adj_list)

    # Example usage of the reverse function
    adj_matrix = [
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [1, 0, 0, 1],
        [0, 0, 1, 0]
    ]
    result = adjacency_matrix_to_list(adj_matrix)
    print(result)