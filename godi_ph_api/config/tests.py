from django.test import TestCase


# Create your tests here.

#
def a_new_decorator(a_func):
    def wrapTheFunction():
        print("aaa")
        a_func()
        print("bbb")

    return wrapTheFunction


def a_function_rd():
    print("1231321321")


# a_function_rd()
#
# a_function_rd = a_new_decorator(a_function_rd)
#
# a_function_rd()

# def a_new_decorator(a_func):
#     def wrapTheFunction():
#         print("I am doing some boring work before executing a_func()")
#
#         a_func()
#
#         print("I am doing some boring work after executing a_func()")
#
#     return wrapTheFunction
#
#
# def a_function_requiring_decoration():
#     print("I am the function which needs some decoration to remove my foul smell")
#
#
# # a_function_requiring_decoration()
# # outputs: "I am the function which needs some decoration to remove my foul smell"
#
# a_function_requiring_decoration = a_new_decorator(a_function_requiring_decoration)
# # now a_function_requiring_decoration is wrapped by wrapTheFunction()
#
# a_function_requiring_decoration()


def func(n):
    if n == 1:
        return 1
    elif n == 2:
        return 2
    else:
        return func(n - 1) + func(n - 2)


def func2(n):
    if n == 1:
        return 1
    elif n == 2:
        return 2
    a = 1
    b = 2
    for i in range(3, n + 1):
        c = a + b
        a = b
        b = c

    return c


# n = int(input())
# if 36 >= n > 0:
#     res = func2(n)
#     print(res)
# else:
#     print(0)


import numpy as np


def func3():
    inp1 = input()
    pNums = inp1.split(",")
    minLo = min(pNums)

    res = np.zeros(len(pNums))
    for i in range(0, len(pNums)):
        if pNums[i] == minLo:
            res[i] == 1
    #

    for i in range(0, len(pNums)):
        if pNums[i] == 1:
            left_fun(0, i, pNums, res)
            right_fun(i, len(pNums), pNums, res)


def left_fun(s, e, pNums, res):
    if s == e:
        return 0
    x = res[e]
    while (s < e):
        if pNums[e - 1] > pNums[e]:
            res[e - 1] = res[e] + x
            x = x + 1
            e = e - 1
        else:
            return 0


def right_fun(s, e, pNums, res):
    pass


# func3()

def choose(n, k):
    res = list(range(1, n - k + 1 + 1))
    res = res[::-1]
    temp = list(range(n - k + 2, n + 1))
    res = res + temp

    print(" ".join(str(i) for i in res))


inp = input()
n, k = inp.split(" ")
choose(int(n), int(k))

