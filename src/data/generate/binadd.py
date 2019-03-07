import itertools
import random
import math
from data.generate.util import make_runner


runner = make_runner("binadd.tm")


def zero_pad(s: str, length: int = 0) -> str:
    return s + ("0" * (length - len(s)))


def int2binstr(i: int) -> str:
    return "".join(reversed("{:b}".format(i)))


def binstr2int(s: str) -> int:
    return 0 if s == "" else int("".join(reversed(s)), base=2)


@runner(step=2, trials=1, description=r"words from $\{1^a \# 1^a \# 0 1^a* \}$ for some $a$")
def accepting_ones(length: int):
    if length <= 2:
        return ["#"] * length
    lengths = [math.ceil((length - 2) / 3) - 1] * 2
    values = ["1" * l for l in lengths]
    values.append(int2binstr(sum([binstr2int(x) for x in values])))
    lengths.append(length - 2 - sum(lengths))
    return list("#".join(zero_pad(x, l)
                         for x, l in zip(values, lengths)))


@runner(step=2, trials=10, description=r"random words from $L(\{0+1\}^* \# \{0+1\}^* \# \{0+1\}^*)$ of length $n$ that are accepted")
def accepting_random(length: int):
    if length <= 2:
        return ["#"] * length
    lengths = [math.ceil((length - 2) / 3) - 1] * 2
    values = ["".join(str(random.randint(0, 1))
                      for x in range(l)) for l in lengths]
    values.append(int2binstr(sum([binstr2int(x) for x in values])))
    lengths.append(length - 2 - sum(lengths))
    return list("#".join(zero_pad(x, l)
                         for x, l in zip(values, lengths)))


@runner(step=2, trials=10, description=r"random words from $L((0+1+\#)^*)$ of length $n$")
def completely_random(length: int):
    return [random.choice(["0", "1", "#"]) for x in range(length)]


@runner(step=2, trials=10, description=r"random words from $L(\{0+1\}^* \# \{0+1\}^* \# \{0+1\}^*)$ of length $n$")
def random_three_numbers(length: int):
    if length <= 2:
        return ["#"] * length
    t = [random.choice(["0", "1"]) for x in range(length)]
    first_hash = random.randint(0, length-1)
    second_hash = random.randint(0, length-1)
    while first_hash == second_hash:
        second_hash = random.randint(0, length-1)
    t[first_hash] = "#"
    t[second_hash] = "#"
    return t
