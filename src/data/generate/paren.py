import itertools
import random
import math
from data.generate.util import make_runner


runner = make_runner("paren.tm")


@runner(step=1, trials=1, description=r'the words $(``(" ``)")^{\lfloor n/2 \rfloor}$ (prepended by $``("$ if $n$ is odd) for all $n$')
def pairs(length: int):
    return ["(", ")"] * (length // 2) + [")"] * (length % 2)


@runner(step=1, trials=1, description=r'the words $``("^{\lceil n/2 \rceil} ``)"^{\lfloor n/2 \rfloor}$ for all $n$')
def nested(length: int):
    return ["("] * math.ceil(length / 2) + [")"] * (length // 2)


@runner(step=1, trials=10, description=r'random words from $L((``("+``)")^*)$ of length $n$')
def completely_random(length: int):
    return ["(" if random.randint(0, 1) == 0 else ")" for x in range(length)]


@runner(step=1, trials=10, description=r"random words of length $n$ that are accepted")
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
