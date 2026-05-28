def verify_card_number(num):
    num = num.replace(' ', '').replace('-', '').replace('_', '') # Remove spaces, dashes, and underscores
    if not num.isdigit():
        return False
    total = 0
    reverse_digits = num[::-1] # Reverse the digits for processing
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1: # Double every second digit from the right
            n *= 2 # If doubling results in a number greater than 9, subtract 9 from it
            if n > 9:
                n -= 9
        total += n
    if total % 10 == 0: # If the total modulo 10 is 0, the number is valid according to the Luhn algorithm
        return 'VALID!'
    else:
        return 'INVALID!'
    
if __name__ == "__main__": # prama: no cover
    num = '453914881'
    num2 = '453_914_881'
    num3 = '453-914-881'
    num4 = '453 914 881'
    print(verify_card_number(num))   # True
    # print(verify_card_number(num2))  # True
    # print(verify_card_number(num3))  # True
    # print(verify_card_number(num4))  # True