from math import floor
from random import random


def has(list: list[any], val: any) -> bool:
    try:
        list.index(val)
        return True
    except:
        return False


def concat(l1, l2):
    l = []
    for i in l1:
        l.append(i)
    for i in l2:
        l.append(i)
    return l


"""
    Pick a random int in [min, max].
"""


def rand_int(min: int, max: int) -> int:
    return floor(random()*(max+1-min))+min


def pick_rand(list: list[any]) -> any:
    return list[rand_int(0, len(list) - 1)]
