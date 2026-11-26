import json
import os
import time
import random

from prime import is_prime, primes_up_to, prime_factorisation, self_test

HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".prime_history.json")
SCORES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".prime_quiz_scores.json")


def _load_history() -> list:
    """Load history from JSON file."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def _save_history(history: list) -> None:
    """Save history to JSON file."""
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)
    except IOError:
        pass


def _add_to_history(entry: dict) -> None:
    """Add an entry to the history and save."""
    history = _load_history()
    history.append(entry)
    _save_history(history)


def _load_scores() -> list:
    """Load quiz scores from JSON file."""
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def _save_scores(scores: list) -> None:
    """Save quiz scores to JSON file, keep top 5."""
    scores.sort(key=lambda s: s["score"], reverse=True)
    top5 = scores[:5]
    try:
        with open(SCORES_FILE, "w") as f:
            json.dump(top5, f, indent=2)
    except IOError:
        pass


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

    is_prime_result = is_prime(num)
    entry = {"type": "check_prime", "number": num, "is_prime": is_prime_result}
    _add_to_history(entry)

    if num < 2:
        print(f"{num} is NOT a prime number. Prime numbers must be greater than or equal to 2.")
    elif is_prime_result:
        print(f"{num} is a prime number.")
    else:
        print(f"{num} is NOT a prime number.")


def handle_list_primes() -> None:
    limit = prompt_int("N: ")
    if limit is None:
        return

    primes = primes_up_to(limit)
    entry = {"type": "list_primes", "limit": limit, "count": len(primes), "primes": [str(p) for p in primes]}
    _add_to_history(entry)

    print(f"Primes up to {limit}:")
    if primes:
        print(", ".join([str(p) for p in primes]))
    else:
        print("None")
    print(f"Count: {len(primes)}")


def handle_factorise() -> None:
    num = prompt_int("Enter a whole number: ")
    if num is None:
        return

    factors = prime_factorisation(num)
    entry = {"type": "factorise", "number": num, "factors": [{"prime": p, "exponent": e} for p, e in factors]}
    _add_to_history(entry)

    if num < 2:
        print(f"{num} has no prime factorisation (must be >= 2).")
    else:
        parts = " x ".join([f"{p}^{e}" if e > 1 else f"{p}" for p, e in factors])
        print(f"{num} = {parts}")


def show_history() -> None:
    """Display the history of prime checks."""
    history = _load_history()
    if not history:
        print("No history found.")
        return

    print("\n=== Prime Check History ===")
    for entry in history:
        etype = entry["type"]
        if etype == "check_prime":
            status = "prime" if entry["is_prime"] else "not prime"
            print(f"  {entry['number']} is {status}")
        elif etype == "list_primes":
            print(f"  Primes up to {entry['limit']}: {entry['count']} primes found")
        elif etype == "factorise":
            parts = " x ".join([f"{factor['prime']}^{factor['exponent']}" if factor['exponent'] > 1 else f"{factor['prime']}" for factor in entry["factors"]])
            print(f"  {entry['number']} = {parts}")


def clear_history() -> None:
    """Clear the history file."""
    _save_history([])
    print("History cleared.")


def handle_self_test() -> None:
    """Run self-test and report results."""
    print("Running self-test...")
    passed = self_test()
    if passed:
        print("Self-test: ALL CHECKS PASSED")
    else:
        print("Self-test: SOME CHECKS FAILED")


def handle_prime_quiz() -> None:
    """Prime Quiz game: pick the prime from four numbers."""
    scores = _load_scores()

    print("\n=== Prime Quiz ===")
    print("Pick the prime number from the four options.")
    print("Score based on speed and accuracy.")
    print("Top 5 scores are saved.")

    while True:
        # Pick a random prime
        prime_candidates = [n for n in range(2, 50) if is_prime(n)]
        if not prime_candidates:
            print("Error: no primes available")
            return
        prime_num = random.choice(prime_candidates)

        # Pick three composite numbers
        composite_candidates = [n for n in range(2, 50) if not is_prime(n)]
        if len(composite_candidates) < 3:
            print("Error: not enough composites")
            return
        composite_nums = random.sample(composite_candidates, 3)

        # Combine and shuffle
        options = [prime_num] + composite_nums
        random.shuffle(options)

        # Ask the question
        start_time = time.time()
        print(f"\nWhich number is prime?")
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")

        choice = input("Your choice (1-4): ").strip()
        try:
            choice_idx = int(choice) - 1
            if choice_idx < 0 or choice_idx >= 4:
                print("Invalid choice. Please choose 1-4.")
                continue
        except ValueError:
            print("Invalid input. Please enter 1-4.")
            continue

        end_time = time.time()
        elapsed = end_time - start_time

        is_correct = options[choice_idx] == prime_num

        if is_correct:
            # Score: bonus for speed, minimum 1 point
            speed_bonus = max(1, int(10 - elapsed))
            score = max(1, speed_bonus)
            print(f"Correct! You earned {score} points (took {elapsed:.1f}s)")
        else:
            print(f"Wrong! The prime was {prime_num}. You earned 0 points.")

        # Add to scores
        scores.append({"prime": prime_num, "score": score if is_correct else 0, "time": elapsed})
        _save_scores(scores)

        # Show top 5
        print("\n=== Top 5 Scores ===")
        for i, s in enumerate(_load_scores(), 1):
            print(f"  {i}. Score: {s['score']} (time: {s['time']:.1f}s)")

        play_again = input("\nPlay again? (y/n): ").strip().lower()
        if play_again != "y":
            break