from tests_coordinate_system import *


def main():
    current_test = 0
    code = ""
    if current_test:
        code = f"test{current_test}()"
    else:
        code = """
for test in [test1, test2, test3, test4, test5, test6]:
    test()
"""
    exec(code)
    pass


if __name__ == "__main__":
    main()
