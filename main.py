from tests_coordinate_system import *


def main():
    current_test = 0
    code = ""
    if current_test:
        exec(f"test{current_test}()")
    else:
        i = 1
        while True:
            try:
                exec(f"test{i}()")
                i += 1
            except Exception as e:
                break


if __name__ == "__main__":
    main()
