def hanoi_solver(n):

    rods = [list(range(n, 0, -1)), [], []] # Initialize the three rods

    moves = [] # List to store the moves

    def move_disk(from_rod, to_rod):
        disk = rods[from_rod].pop() # Remove the top disk from the source rod
        rods[to_rod].append(disk) # Place it on the target rod
        moves.append(f"{rods[0]} {rods[1]} {rods[2]}") # Record the current state of the rods