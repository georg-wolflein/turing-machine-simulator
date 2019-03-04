import itertools
import random
from data.generate.util import make_runner


runner = make_runner("binadd.tm")


@runner(step=2, trials=10, description=r"random words from $L((0+1+\#)^*)$ of length $n$")
def completely_random(length: int):
    return [random.choice(["0", "1", "#"]) for x in range(length)]


@runner(step=2, trials=10, description=r"random words from $L(\{0+1\}^* # \{0+1\}^* # \{0,1\}^*)$ of length $n$")
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


@runner(step=2, trials=10, description=r"random words from $L(\{0+1\}^* \# \{0+1\}^* \# \{0,1\}^*)w$ of length $n$ that are accepted")
def accepting_three_numbers(length: int):
    def int2binstr(i: int, length: int) -> str:
        s = "{:b}".format(i)
        return s + "".join("0" * (length - len(s)))
    if length <= 2:
        return ["#"] * length
    lengths = random.sample(range(length - 2), 2)
    values = [random.randint(0, 2 ** l - 1) for l in lengths]
    lengths.append(length - 2 - sum(lengths))
    values.append(sum(values))
    return list("#".join(int2binstr(x, l) for x, l in zip(values, lengths)))
