from prime_handlers import handle_check_prime, handle_list_primes

def print_menu() -> None:
    print("\n=== Prime Number Checker ===")
    print("1. Check if a number is prime")
    print("2. List primes up to N")
    print("3. Exit")

def main() -> None:
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            handle_check_prime()
        elif choice == "2":
            handle_list_primes()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()