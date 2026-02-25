# Write a python program to print table of a number which lies between 1 and 10 using match case statements

num = int(input("Enter a number between 1 and 10: "))

match num:
    case 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10:
        print(f"\nMultiplication Table of {num}:\n")
        for i in range(1, 11):
            print(f"{num} x {i} = {num * i}")
    case _:
        print("Invalid input! Please enter a number between 1 and 10.")