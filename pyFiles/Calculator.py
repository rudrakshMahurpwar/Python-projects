import math

print("Hello This Calculator performs various fuctions")
def menu():        
    print(r"""
1. Addition: +
2. Substraction: -
3. Multiplicaiton: *
4. Divsion: /
5. Moduls: %
6. Floor Division: //
7. Power: **
8. Square Root: sqrt
9. Logrithm: log
10. Factorial: fact
    """)
while True:
    menu()
    try:
        num1 = float(input("Enter first number: "))
        op = input("Enter the operator number or symbol: ")
        binaryop = ['sqrt' , '8' , 'log' , '9' , 'fact' , '10']
        if op in binaryop:
            match op:
                case 'sqrt' | '8':
                    print(f"The square root of {num1} is: ", math.sqrt(num1))
                case 'log' | '9':
                    print(f"The logarithm of {num1} is: ", math.log(num1))
                case 'fact' | '10':
                    print(f"The factorial of {num1} is: ", math.factorial(int(num1)))
                case _:
                    print("Invalid operator")
                    continue
        else:
            num2 = float(input("Enter second number: "))
            match op:
                case '+' | '1':
                    print(f"The addition of {num1} and {num2} is: ", num1+num2)
                case '-' | '2':
                    print(f"The substraction of {num1} and {num2} is: ", num1-num2)
                case '*' | '3':
                    print(f"The multiplication of {num1} and {num2} is: ", num1*num2)
                case '/' | '4':
                    print(f"The division of {num1} and {num2} is: ", num1/num2)
                case '%' | '5':
                    print(f"The modulus of {num1} and {num2} is: ", num1%num2)
                case '//' | '6':
                    print(f"The floor division of {num1} and {num2} is: ", num1//num2)
                case '^' | '7':
                    print(f"The power of {num1} and {num2} is: ", num1**num2)
                case _:
                    print("Invalid operator")

    except ValueError:
        print("Enter correct values")
    except ZeroDivisionError:
        print("Zero Division Error")
    except Exception as e:
        print(e)
