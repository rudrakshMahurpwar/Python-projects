def solid_square(rows, columns):
    # Solid Square
    for _ in range(1, rows + 1):
        # print("* " * columns)
        for _ in range(1, columns + 1):
            print("*", end=" ")
        print()


def right_triangle(rows, columns):
    # Right Tringle
    for i in range(1, rows + 1):
        # print("* " * i)
        for _ in range(i):
            print("*", end=" ")
        print()


def inverted_right_triangle(rows, columns):
    # Inverted Right Triangle
    for i in range(rows, 0, -1):
        for _ in range(i):
            print("*", end=" ")
        print()


def left_triangle(rows, columns):
    # Left Triangle
    for i in range(rows, 0, -1):
        for _ in range(i):
            print(" ", end=" ")
        for _ in range((rows - i) + 1):
            print("*", end=" ")
        print()


def inverted_left_triangle(rows, columns):
    # Inverted Left Triangle
    for i in range(rows, 0, -1):
        # print(" " * (rows - i), end="")
        # print("* " * i)
        for _ in range(rows - i):
            print(" ", end=" ")
        for _ in range(i):
            print("*", end=" ")
        print()


def straight_line(columns):
    # Straingt Line
    print("* " * columns)


def number_triangle(rows, columns):
    # Number Triangle
    for i in range(1, rows + 1):
        for j in range(i):
            print(j, end=" ")
        print()


def repeating_number_triangle(rows, columns):
    # Repeating Number Triangle
    for i in range(1, rows + 1):
        for _ in range(i):
            print(i, end=" ")
        print()


def continuous_number(rows, columns):
    # Continous Number
    start_number = 1
    for i in range(1, rows + 1):
        for _ in range(i):
            print(start_number, end=" ")
            start_number += 1
        print()


def pyramid(rows, columns):
    # Pyramid
    for i in range(1, rows + 1):
        for _ in range(rows - i):
            print(" ", end=" ")
        for _ in range(2 * i - 1):
            print("*", end=" ")
        print()


def inverted_pyramid(rows, columns):
    # Inverted Pyramid
    for i in range(1, rows + 1):
        for _ in range(i - 1):
            print(" ", end=" ")
        for _ in range(2 * (rows - i) + 1):
            print("*", end=" ")
        print()


def diamond(rows, cloumns):
    # Diamond
    for i in range(1, rows):
        print("  " * (rows - i), end=" ")
        print("* " * (2 * i - 1), end=" ")
        print()
    for i in range(1, rows + 1):
        print("  " * (i - 1), end=" ")
        print("* " * (2 * (rows - i) + 1), end=" ")
        print()


def hollow_square(rows, columns):
    # Hollow Square
    for i in range(1, rows + 1):
        (
            print("* " * columns)
            if (i == rows or i == 1)
            else print("* " + ("  " * (columns - 2)) + "* ")
        )


def hollow_right_triangle(rows, columns):
    # Hollow Right Triangle
    for i in range(1, rows + 1):
        (
            print("* " * i)
            if i == 1 or i == rows
            else print("* " + ("  " * (i - 2)) + "* ")
        )


def grid(rows, columns):
    # Grid
    for i in range(1, rows + 1):
        print(" | ".join([" "] * columns))
        print("-" * (columns * 4))


if __name__ == "__main__":
    # rows = int(input("Input Number of rows: "))
    # columns = int(input("Input Number of columns: "))

    print("Printing Patterns Designs.")

    # solid_square(rows, columns)
    # print("Solid Square\n")
    # right_triangle(rows, columns)
    # print("Right Triangle\n")
    # inverted_right_triangle(rows, columns)
    # print("Inverted Right Triangle\n")
    # left_triangle(rows, columns)
    # print("Left Triangle\n")
    # inverted_left_triangle(rows, columns)
    # print("Inverted Left Triangle\n")
    # straight_line(columns)
    # print("Straight Line\n")
    # number_triangle(rows, columns)
    # print("Number Triangle\n")
    # repeating_number_triangle(rows, columns)
    # print("Repeating Number Tringle\n")
    # continuous_number(rows, columns)
    # print("Continous Number\n")
    # pyramid(rows, columns)
    # print("Pyramid\n")
    # inverted_pyramid(rows, columns)
    # print("Inverted Pyramid\n")
    # diamond(rows, columns)
    # print("Diamond\n")
    # hollow_square(rows, columns)
    # print("Hollow Square\n")
    # hollow_right_triangle(rows, columns)
    # print("Hollow Right Triangle")
    # grid(rows, columns)
    # print("Grid")
