from tests_coordinate_system import *


def start_test(i):
    exec(f"test{i}()")


def main():
    current_test = "_rotate_to_local_angle"
    current_test = "_spiral_spring"
    current_test = 0
    if current_test:
        exec(f"test{current_test}()")
    else:
        i = 1
        while True:
            try:
                start_test(i)
                i += 1
            except Exception as e:
                break


if __name__ == "__main__":
    main()
