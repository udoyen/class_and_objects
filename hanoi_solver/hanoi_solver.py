def hanoi_solver(n):
    
    # Initialize the three rods
    rods = [list(range(n, 0, -1)), [], []] # Rod 0 starts with all disks, Rod 1 and Rod 2 are empty
    moves = []

    def move_disk(from_rod, to_rod):
        """
        Move the top disk from 'from_rod' to 'to_rod' and record the move."""
        disk = rods[from_rod].pop()
        rods[to_rod].append(disk)
        moves.append(f"{rods[0]} {rods[1]} {rods[2]}")

    def solve_hanoi(num_disks, from_rod, to_rod, aux_rod): # 0, 2, 1
        """
        Recursive function to solve the Tower of Hanoi problem."""
        if num_disks == 1: # Base case: just move one disk directly
            move_disk(from_rod, to_rod)
            return
        solve_hanoi(num_disks - 1, from_rod, aux_rod, to_rod) # Move top n-1 disks to auxiliary rod 0, 1, 2
        move_disk(from_rod, to_rod) # Move the nth disk to target rod
        solve_hanoi(num_disks - 1, aux_rod, to_rod, from_rod) # Move n-1 disks from auxiliary rod to target rod 1, 2, 0

    if n > 0: # Only solve if there are disks to move
        moves.append(f"{rods[0]} {rods[1]} {rods[2]}") # Initial state
        solve_hanoi(n, 0, 2, 1) # Solve the puzzle
    else:
        return "[] [] []" # Handle the case for 0 disks

    return "\n".join(moves)


if __name__ == "__main__": # pragma: no cover
    # Example usage:
    n = 6
    print(hanoi_solver(n))