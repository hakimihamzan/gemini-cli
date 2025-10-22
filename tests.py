from functions.get_files_info import get_files_info


def main():
    try:
        get_files_info("calculator", ".")

    except Exception as e:
        print("Result for current directory:")
        print(f"Error: {e}")
        print("\n")

    try:
        get_files_info("calculator", "pkg")

    except Exception as e:
        print("Result for current directory:")
        print(f"Error: {e}")
        print("\n")

    try:
        get_files_info("calculator", "../")

    except Exception as e:
        print("Result for current directory:")
        print(f"Error: {e}")
        print("\n")

    try:
        get_files_info("calculator", "/bin")

    except Exception as e:
        print("Result for current directory:")
        print(f"Error: {e}")
        print("\n")


if __name__ == "__main__":
    main()
