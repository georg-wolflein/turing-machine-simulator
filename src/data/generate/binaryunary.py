'''Benchmarks for the binaryunary machine.
'''

import itertools
import random
import math
from data.generate.runner import make_runner


runner = make_runner("binaryunary.tm")


@runner(iterations=16, trials=1, description=r"words in the form $1^n$")
def ones(length: int):
    print(length)
    return ["1"] * length


@runner(trials=1, description=r"words in the form $0^n$")
def zeros(length: int):
    return ["0"] * length


@runner(trials=10, description=r"random words from $L(\{0+1\}^*)$ of length $n$")
def completely_random(length: int):
    return [random.choice(["0", "1"]) for _ in range(length)]
