print("Hello world")


def add_two_nums(a: int, b: int):
    if isinstance(a, (int, float)) and isinstance(b, (int,float)):
        return a+b
    raise Exception
