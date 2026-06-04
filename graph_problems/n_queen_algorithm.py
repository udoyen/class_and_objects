def dfs_n_queens(n):
    if n < 1: 
        return []
    results = []

    def is_safe(row, col, current_board):
        for past_row, past_col in enumerate(current_board):
            if past_col == col or abs(past_col - col) == abs(past_row - row):
                return False
        return True
    def solve(row, current_board):
        '''Helper function to perform DFS and backtracking.
        row: current row we are trying to place a queen in
        current_board: A list of columns where queens have already been placed. (e.g., [1, 3] means Row 0 has a queen in Col 1, 
        and Row 1 has a queen in Col 3)'''
        if row == n:
            results.append(current_board[:])  # Found a valid solution
            return
        for col in range(n):
            if is_safe(row, col, current_board):
                current_board.append(col)
                solve(row + 1, current_board)  # Recur to place queen in the next row
                current_board.pop()  # Backtrack
    solve(0, [])
    return results

if __name__ == "__main__":
    n = 8
    solutions = dfs_n_queens(n)
    print(f"Total solutions for {n}-Queens: {len(solutions)}")
    for solution in solutions:
        print(solution)