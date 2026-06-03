def dfs(matrix, start_node):
    stack = [start_node]
    visited = []
    while stack:
        current_node = stack.pop()
        if current_node not in visited:
            visited.append(current_node)

            # Add neighbors to the stack
            for i in range(len(matrix)):
                if matrix[current_node][i] == 1:
                    stack.append(i)
    return visited


if __name__ == "__main__": # pragma: no cover
    # Example usage
    graph = [
        [0, 1, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [0, 0, 1, 0]
    ]
    start_node = 1
    print(dfs(graph, start_node))