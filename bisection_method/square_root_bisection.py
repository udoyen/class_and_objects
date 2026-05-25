def square_root_bisection(target, tolerance=0.01, max_iterations=1000):
    """Calculates the square root of a non-negative number using the bisection method."""
    if target < 0:
        raise ValueError("Square root of negative number is not defined in real numbers")
    
    if target == 0 or target == 1:
        print(f"The square root of {target} is {target}")
        return target
    
    low = 0.0
    high = max(1.0, float(target))
    
    for iteration in range(1, max_iterations + 1):
        # 1. Calculate the current guess
        guess = (low + high) / 2.0
        
        # 2. Check if the distance between bounds is smaller than the tolerance
        if (high - low) <= tolerance:
            print(f"The square root of {target} is approximately {guess}")
            return guess
            
        # 3. Adjust boundaries if we need to keep searching
        if guess**2 < target:
            low = guess
        else:
            high = guess
            
    # If it loops max_iterations without converging
    print(f"Failed to converge within {max_iterations} iterations")
    return None


if __name__ == '__main__': # pragma: no cover
    square_root_bisection(0.001, 0.0000001, 50)
