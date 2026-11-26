# Prime Kit

Prime Kit is a small command line program for working with prime numbers.

## What this program does

You can:

1. **Check if a number is prime** - Determines if a given number is prime
2. **List primes up to N** - Lists all prime numbers up to a given limit
3. **Prime factorisation** - Shows the prime factorisation of a number (e.g., `360 = 2^3 x 3^2 x 5`)
4. **Self-test** - Runs a self-test checking `is_prime` and `prime_factorisation` against known lists of primes and composites, and reports any disagreement
5. **Show history** - Displays a history of all prime checks, factorisations, and prime lists made in the current and previous sessions; data is saved between sessions in `.prime_history.json`
6. **Clear history** - Clears the saved history file
7. **Prime Quiz** - A game where you pick the prime number from four options; scores based on speed and accuracy; top 5 scores are saved to `.prime_quiz_scores.json`

A prime number is a whole number greater than 1 that can only be divided evenly by 1 and by itself. Examples: 2, 3, 5, 7, 11, 13.

The program runs in a terminal. It does not need the internet. It saves data between sessions using JSON files in the project directory.

## What is in this project

| File | Job |
| --- | --- |
| `main.py` | Shows the menu and keeps the program running until you choose exit. |
| `prime_handlers.py` | Reads your numbers, checks they are valid, and prints the results. |
| `prime.py` | Does the actual prime number work. It knows nothing about menus or printing. |
| `README.md` | This guide. |

## What you need

Python 3.10 or newer.

This project was checked with Python 3.13.12. You can check your own version with:

```bash
python3 --version
```

There is nothing to install. No setup step is needed.

## How to run it

From this folder, run:

```bash
python3 main.py
```

You will see:

```text
=== Prime Number Checker ===
1. Check if a number is prime
2. List primes up to N
3. Prime factorisation
4. Self-test
5. Show history
6. Clear history
7. Prime Quiz
8. Exit
```

Type `1`-`8` and press Enter.

### Example 1: check one number

```text
Choose an option: 1
Enter a whole number: 17
17 is a prime number.
```

If the number is not prime:

```text
Choose an option: 1
Enter a whole number: 18
18 is NOT a prime number.
```

If the number is less than 2:

```text
Choose an option: 1
Enter a whole number: 1
1 is NOT a prime number. Prime numbers must be greater than or equal to 2.
```

### Example 2: prime factorisation

```text
Choose an option: 3
Enter a whole number: 360
360 = 2^3 x 3^2 x 5
```

### Example 3: list primes up to a number

```text
Choose an option: 2
N: 10
Primes up to 10:
2, 3, 5, 7
Count: 4
```

If the number is 1 or less, there are no primes to show:

```text
Choose an option: 2
N: -5
Primes up to -5:
None
Count: 0
```

### Example 4: self-test

```text
Choose an option: 4
Running self-test...
=== Self-Test: is_prime ===

=== Self-Test: prime_factorisation ===
  OK: 2 = 2
  OK: 3 = 3
  OK: 4 = 2^2
  OK: 6 = 2 x 3
  OK: 12 = 2^2 x 3
  OK: 360 = 2^3 x 3^2 x 5
  OK: 49 = 7^2
  OK: 97 = 97
  OK: 100 = 2^2 x 5^2

All tests passed!
Self-test: ALL CHECKS PASSED
```

### Example 5: show history

After running checks, option 5 shows:

```text
=== Prime Check History ===
  17 is prime
  360 = 2^3 x 3^2 x 5
  Primes up to 10: 4 primes found
```

### Example 6: Prime Quiz

```text
Choose an option: 7
=== Prime Quiz ===
Pick the prime number from the four options.
Score based on speed and accuracy.
Top 5 scores are saved.

Which number is prime?
  1. 30
  2. 8
  3. 31
  4. 45
Your choice (1-4): Correct! You earned 9 points (took 1.0s)

=== Top 5 Scores ===
  1. Score: 9 (time: 1.0s)

Play again? (y/n): n
```

If you type anything other than `1`-`8`, the program says:

```text
Invalid option. Please choose 1, 2, 3, 4, 5, 6, 7, or 8.
```

If you type something that is not a whole number where a number is asked for, the program says:

```text
Invalid input. Please enter a whole number (e.g., 7, 17).
```

## How the program works

Here is the path a request takes:

```text
You type a choice
       |
       v
main.py shows the menu and reads your choice
       |
       v
prime_handlers.py asks for the number and checks it is a whole number
       |
       v
prime.py does the prime number work
       |
       v
prime_handlers.py prints the answer
       |
       v
main.py shows the menu again
```

The three files each do one part. That is the main design choice in this project.

## Design choices, one by one

### 1. Keep the menu separate from the prime work

`main.py` only handles the menu. It does not know how to find a prime number.

Why this was chosen:

- If you later want a different menu, you only change `main.py`.
- If you later want to change how primes are found, you only change `prime.py`.
- A mistake in the menu cannot break the prime math, and a mistake in the prime math cannot break the menu.

This is why `main.py` calls small functions in `prime_handlers.py`: `handle_check_prime()`, `handle_list_primes()`, `handle_factorise()`, `handle_self_test()`, `show_history()`, `clear_history()`, and `handle_prime_quiz()`. It does not call the prime functions directly.

### 2. Put the "ask and print" work in its own file

`prime_handlers.py` sits between the menu and the math.

It does three things:

- Asks you for a number with `input()`.
- Turns your text into a whole number with `int()`. If that fails, it prints a friendly message and returns `None`. `None` means "there is no number to work with".
- Prints the final answer in plain words.

Why this was chosen:

- The same number checking is used by both menu options, so it lives in one place: `prompt_int()`.
- `prime.py` stays clean. It can be used by another program later without printing anything to the screen.

For example, `is_prime(17)` gives back `True`. It does not print. The printing happens in `prime_handlers.py`.

### 3. Use two different ways to find primes

The project has two jobs, and each job uses the method that fits it best.

**Job 1: check one number.** This uses `is_prime()` in `prime.py`.

The steps are simple:

- Numbers below 2 are not prime.
- 2 is prime.
- Any other even number is not prime.
- For an odd number, try dividing by 3, 5, 7, and so on. Stop when the divisor multiplied by itself is bigger than the number. If nothing divided it evenly, it is prime.

Why stop there? If a number has a divisor bigger than that point, it must also have a smaller partner divisor. That smaller one would already have been checked.

**Job 2: list all primes up to N.** This uses `primes_up_to()` and `prime_sieve()` in `prime.py`.

The sieve works like crossing numbers off a list:

- Write down every number from 0 to N and mark each one as "maybe prime".
- Mark 0 and 1 as not prime.
- Start with 2. It is prime, so cross out 2 x 2, 2 x 3, 2 x 4, and so on. These are all divisible by 2.
- Move to the next number still marked "maybe prime". Cross out its multiples too.
- Stop when the starting number multiplied by itself is bigger than N.
- The numbers left marked "maybe prime" are the primes.

Why not just call `is_prime()` for every number? That would work, but the sieve reuses work it already did. When it crosses out multiples of 2, it never has to test those numbers again. For a long list, this saves a lot of repeated checking.

### 4. Let the math functions return answers, not messages

`prime.py` returns simple answers:

- `is_prime(num)` gives back `True` or `False`.
- `prime_sieve(max_n)` gives back a list of `True` and `False` flags, one for each number from 0 to max_n.
- `primes_up_to(limit)` gives back the list of primes, for example `[2, 3, 5, 7]` for 10.
- `prime_factorisation(n)` gives back a list of `(prime, exponent)` tuples, for example `[(2, 3), (3, 2), (5, 1)]` for 360.

Why this was chosen:

- The same answer can be shown in different ways later. For example, you could show a count, a list, or a web page without changing the math.
- It is easy to check these functions in isolation.

### 5. Handle bad input early

The program checks input at the point where it is read, in `prime_handlers.py`.

- A menu choice that is not `1`-`8` is rejected in `main.py`, because that is where the menu lives.
- A number that is not a whole number is rejected in `prompt_int()`.
- A number below 2 is rejected only for the "check one number" option, because primes must be at least 2.
- For the "list primes" option, a number below 2 is allowed and gives an empty result: `None` and `Count: 0`.

Why this was chosen:

- The math functions never have to deal with unclear text like `"abc"`.
- The user gets a clear message and can try again right away.

### 6. Keep the menu running after a mistake

`main.py` uses a `while True` loop. That means "keep doing this until we are told to stop". The only way out is choosing `8`.

Why this was chosen:

- A typo does not force you to restart the program.
- The exit path is simple and visible: option 8 prints `Goodbye!` and ends the loop.

### 7. No extra packages, minimal saved data

The project uses only Python itself standard library modules (`json`, `os`, `time`, `random`).

Why this was chosen:

- It runs anywhere Python 3.10 or newer is available.
- There is no install step and no network access.
- Data is saved between sessions using JSON files (`.prime_history.json` and `.prime_quiz_scores.json`) in the project directory.

## Things to know

- Only whole numbers are accepted. `7` is fine; `7.5` is not.
- Very large numbers take longer and use more memory, especially in the "list primes" option. The sieve needs one entry for every number from 0 up to N.
- The self-test checks your algorithms against known lists - if any fail, it will report them.
- The history is saved between sessions in `.prime_history.json` in the project directory.
- The Prime Quiz top 5 scores are saved in `.prime_quiz_scores.json` in the project directory.
- Very large numbers take longer, especially in the "list primes" option. The sieve needs one entry for every number from 0 up to N.

## Where to make changes

- To change the words in the menu: `main.py`.
- To change how numbers are asked for or how results are printed: `prime_handlers.py`.
- To change how primes are found: `prime.py`.