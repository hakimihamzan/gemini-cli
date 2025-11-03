from functions.run_python_file import run_python_file


def test():
    print("\n")
    result = run_python_file("calculator", "main.py")
    print(result)
    print("\n")

    # result = run_python_file("calculator", "tests.py")
    # print(result)
    # print('\n')

    result = run_python_file("calculator", "../main.py")
    print(result)
    print("\n")

    result = run_python_file("calculator", "nonexistent.py")
    print(result)
    print("\n")

    result = run_python_file("calculator", "lorem.txt")
    print(result)
    print("\n")


if __name__ == "__main__":
    test()
