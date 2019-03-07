import itertools
import random
import math
from data.generate.util import make_runner


runner = make_runner("subword.tm", "subword_fast.tm")


@runner(step=2, trials=1, description=r"words from $\{w\#w \mid w \in \{0,1\}^{ \lfloor n/2 \rfloor } \}$")
def equal(length: int):
    if length <= 1:
        return ["#"] * length
    a = [random.choice(["0", "1"]) for _ in range((length - 1) // 2)]
    b = a.copy()
    while len(a) + len(b) + 1 < length:
        a.append(random.choice(["0", "1"]))
    return a + ["#"] + b


@runner(step=2, trials=10, description=r"random words from $L(\{0+1\}^* \# \{0+1\}^*)$ of length $n$ that are accepted")
def accepting_random(length: int):
    if length <= 1:
        return ["#"] * length
    a = [random.choice(["0", "1"]) for _ in range((length - 1) // 2)]
    b = [random.choice(["0", "1"]) for _ in range((length - 1) // 2)]
    while len(a) + len(b) + 1 < length:
        a.append(random.choice(["0", ""]))
    return a + ["#"] + b


@runner(step=2, trials=10, description=r"random words from $L((0+1+\#)^*)$ of length $n$")
def completely_random(length: int):
    return [random.choice(["0", "1", "#"]) for x in range(length)]
