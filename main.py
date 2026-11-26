from prime_handlers import (
    handle_check_prime,
    handle_list_primes,
    handle_factorise,
    handle_self_test,
    show_history,
    clear_history,
)


def print_menu() -> None:
    print("\n=== Prime Number Checker ===")
    print("1. Check if a number is prime")
    print("2. List primes up to N")
    print("3. Prime factorisation")
    print("4. Self-test")
    print("5. Show history")
    print("6. Clear history")
    print("7. Prime Quiz")
    print("8. Exit")

def main() -> None:
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            handle_check_prime()
        elif choice == "2":
            handle_list_primes()
        elif choice == "3":
            handle_factorise()
        elif choice == "4":
            handle_self_test()
        elif choice == "5":
            show_history()
        elif choice == "6":
            clear_history()
        elif choice == "7":
            from prime_handlers import handle_prime_quiz
            handle_prime_quiz()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1, 2, 3, 4, 5, 6, 7, or 8.")


if __name__ == "__main__":
    main()