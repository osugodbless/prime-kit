# Single prime number check
def is_prime(num: int) -> bool:
    if num < 2:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False

    sq = 3
    while sq * sq <= num:
        if num % sq == 0:
            return False
        sq += 2

    return True

# Implementation of Eratosthenes sieve for checking primes in a range of number up to the max number
def prime_sieve(max_n: int) -> list[bool]:
    if max_n < 0:
        return []

    is_prime_table = [True] * (max_n + 1)
    is_prime_table[0] = False
    
    if max_n >= 1:
        is_prime_table[1] = False

    p = 2
    while p * p <= max_n:
        if is_prime_table[p]:
            for multiple in range(p * p, max_n + 1, p):
                is_prime_table[multiple] = False
        p += 1

    return is_prime_table


# Return all prime numbers from 2 up to limit (limit inclusive)
def primes_up_to(limit: int) -> list[int]:
    if limit < 2:
        return []

    sieve = prime_sieve(limit)
    return [n for n in range(2, limit + 1) if sieve[n]]


# Return the prime factorisation of n as a list of (prime, exponent) tuples
def prime_factorisation(n: int) -> list[tuple[int, int]]:
    if n < 2:
        return []

    factors: list[tuple[int, int]] = []
    # Handle factor 2
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    if count > 0:
        factors.append((2, count))

    # Odd factors starting from 3
    f = 3
    while f * f <= n:
        count = 0
        while n % f == 0:
            n //= f
            count += 1
        if count > 0:
            factors.append((f, count))
        f += 2

    # If n is still > 1, it is a prime factor
    if n > 1:
        factors.append((n, 1))

    return factors


# Known primes and composites for self-test
_PRIMES_UNDER_100 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
_COMPOSITES_UNDER_100 = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30, 32, 33, 34, 35, 36, 38, 39, 40, 42, 44, 45, 46, 48, 49, 50, 51, 52, 54, 55, 56, 57, 58, 60, 62, 63, 64, 65, 66, 68, 69, 70, 72, 74, 75, 76, 77, 78, 80, 81, 82, 84, 85, 86, 87, 88, 90, 91, 92, 93, 94, 95, 96, 98, 99]


def self_test() -> bool:
    """Run self-test checking is_prime and prime_factorisation against known lists."""
    all_pass = True

    print("=== Self-Test: is_prime ===")
    for n in _PRIMES_UNDER_100:
        result = is_prime(n)
        if not result:
            print(f"  FAIL: {n} should be prime")
            all_pass = False
    for n in _COMPOSITES_UNDER_100:
        result = is_prime(n)
        if result:
            print(f"  FAIL: {n} should not be prime")
            all_pass = False

    print("\n=== Self-Test: prime_factorisation ===")
    test_cases = [2, 3, 4, 6, 12, 360, 49, 97, 100]
    for n in test_cases:
        factors = prime_factorisation(n)
        # Verify factorisation product equals n
        product = 1
        for p, e in factors:
            product *= p ** e
        if product != n:
            print(f"  FAIL: {n} factorisation product {product} != {n}")
            all_pass = False
        else:
            print(f"  OK: {n} = {' x '.join([f'{p}^{e}' if e > 1 else f'{p}' for p, e in factors])}")

    if all_pass:
        print("\nAll tests passed!")
    else:
        print("\nSome tests FAILED!")
    return all_pass
