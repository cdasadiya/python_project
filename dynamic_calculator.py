"""Dynamic calculator supporting add, subtract, multiply, and divide operations."""


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b


def get_number(prompt: str) -> float:
    while True:
        raw_value = input(prompt).strip()
        try:
            return float(raw_value)
        except ValueError:
            print("Invalid number. Please enter a valid numeric value.")


def run_calculator() -> None:
    operations = {
        "1": ("Addition", add),
        "2": ("Subtraction", subtract),
        "3": ("Multiplication", multiply),
        "4": ("Division", divide),
    }

    print("Dynamic Calculator")
    print("------------------")

    while True:
        print("\nChoose an operation:")
        for key, (name, _) in operations.items():
            print(f"{key}. {name}")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "5":
            print("Thank you for using Dynamic Calculator!")
            break

        if choice not in operations:
            print("Invalid choice. Please select from 1 to 5.")
            continue

        num1 = get_number("Enter the first number: ")
        num2 = get_number("Enter the second number: ")

        operation_name, operation_func = operations[choice]
        try:
            result = operation_func(num1, num2)
            print(f"Result of {operation_name}: {result}")
        except ZeroDivisionError as error:
            print(error)


if __name__ == "__main__":
    run_calculator()
