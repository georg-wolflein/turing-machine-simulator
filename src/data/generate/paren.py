import itertools
import random
from data.generate.util import make_runner


runner = make_runner("paren.tm")


@runner(step=2, trials=1, description=r"the words $(``(´´ ``)´´)^{\lfloor n/2 \rfloor}$ for all $n$")
def accepting_pairs(length: int):
    return ["(", ")"] * (length // 2)


@runner(step=2, trials=1, description=r"the words $``(´´^{\lfloor n/2 \rfloor} ``)´´^{\lfloor n/2 \rfloor}$ for all $n$")
def accepting_nested(length: int):
    return ["("] * (length // 2) + [")"] * (length // 2)


@runner(step=2, trials=10, description=r"random words from $L((``(´´+``)´´)^*)$ of length $n$")
def completely_random(length: int):
    return ["(" if random.randint(0, 1) == 0 else ")" for x in range(length)]


@runner(step=2, trials=10, description=r"random words of length $n$ that are accepted")
def accepting_random(length: int):
    result = []
    n_open = 0
    n_closed = 0
    while n_open <= (length // 2):
        if n_open > n_closed:
            if random.randint(0, 1) == 0:
                n_open += 1
                result.append("(")
            else:
                n_closed += 1
                result.append(")")
        else:
            n_open += 1
            result.append("(")
    return result + [")"] * (n_open - n_closed)
