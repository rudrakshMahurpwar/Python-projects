def get_operand(number):
    while True:
        try:
            return float(input(f"Enter operand {number}: "))
        except ValueError:
            print("Enter a valid number!")


def get_operation():
    valid_operations = ["+", "-", "*", "/", "%", "**"]
    while True:
        op = input("Enter operation (+, -, *, /, %, **): ").strip()
        if op in valid_operations:
            return op
        print("Invalid operation! Try again.")


def perform_calculation(operand1, operation, operand2):
    match operation:
        case "+":
            return operand1 + operand2
        case "-":
            return operand1 - operand2
        case "*":
            return operand1 * operand2
        case "/":
            if operand2 == 0:
                return "Error: Division by zero!"
            else:
                return operand1 / operand2
        case "%":
            if operand2 == 0:
                return "Error: Division by zero!"
            else:
                return operand1 % operand2
        case "**":
            return operand1**operand2
        case _:
            return None


if __name__ == "__main__":
    calculate = True
    while calculate:
        calculate = input("Calculate?(y/n): ").strip().lower()
        if calculate == "y":
            operand1 = get_operand(1)
            operation = get_operation()
            operand2 = get_operand(2)
            result = perform_calculation(operand1, operation, operand2)

            print("Result:", result)
        elif calculate == "n":
            print("Goodbye!")
            break
        else:
            print("Please enter 'y' or 'n'.")
