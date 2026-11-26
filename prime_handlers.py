from prime import is_prime, primes_up_to

def prompt_int(message: str) -> int | None:
    """Prompt the user for a whole number. Returns None if input is invalid."""
    raw = input(message).strip()
    try:
        return int(raw)
    except ValueError:
        print("Invalid input. Please enter a whole number (e.g., 7, 17).")
        return None


def handle_check_prime() -> None:
    num = prompt_int("Enter a whole number: ")
    if num is None:
        return

    if num < 2:
        print(f"{num} is NOT a prime number. Prime numbers must be greater than or equal to 2.")
    elif is_prime(num):
        print(f"{num} is a prime number.")
    else:
        print(f"{num} is NOT a prime number.")


def handle_list_primes() -> None:
    limit = prompt_int("N: ")
    if limit is None:
        return

    primes = primes_up_to(limit)
    print(f"Primes up to {limit}:")
    if primes:
        print(", ".join([str(p) for p in primes]))
    else:
        print("None")
    print(f"Count: {len(primes)}")
