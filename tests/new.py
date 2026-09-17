from math import sqrt


def lenght(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


a = [float(input("a[0] = ")), float(input("a[1] = "))]
b = [float(input("b[0] = ")), float(input("b[1] = "))]
c = [float(input("c[0] = ")), float(input("c[1] = "))]
print(lenght(a, b) + lenght(b, c) + lenght(a, c))
