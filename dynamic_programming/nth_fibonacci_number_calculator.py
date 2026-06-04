def fibonacci(n):
    sequence = [0, 1]

    # check the number is positive
    if n <= 1:
        return sequence[n]
    # calculate the Fibonacci sequence iteratively until we reach the nth number
    for i in range(2, n + 1):
        sequence.append(sequence[i - 1] + sequence[i - 2])
    return sequence[n]

if __name__ == "__main__": # pragma: no cover
    n = 10
    print(f"The {n}th Fibonacci number is: {fibonacci(n)}")