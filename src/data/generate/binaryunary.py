import itertools
import random
import math
from data.generate.util import make_runner


runner = make_runner("binaryunary.tm")


@runner(step=1, trials=1, description=r"words in the form $1^n$")
def ones(length: int):
    return ["1"] * length


@runner(step=1, trials=1, description=r"words in the form $0^n$")
def zeros(length: int):
    return ["0"] * length


@runner(step=1, trials=10, description=r"random words from $L(\{0+1\}^*)$ of length $n$")
def completely_random(length: int):
    return [random.choice(["0", "1"]) for _ in range(length)]
