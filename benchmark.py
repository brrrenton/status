#!/usr/bin/python3

from status import status

if __name__ == "__main__":
    import timeit

    n = 10
    print(timeit.timeit("status()", globals=globals(), number=n) / n)
