# test_script.py

# Function to calculate the factorial of a number
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

# Function to check if a number is prime
def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

# Main script logic
if __name__ == "__main__":
    print("Factorials:")
    for i in range(6):
        print(f"{i}! = {factorial(i)}")

    print("\nPrime Numbers:")
    for i in range(20):
        if is_prime(i):
            print(f"{i} is a prime number")
