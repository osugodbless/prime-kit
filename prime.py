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