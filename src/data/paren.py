import itertools
import random
from data.util import make_runner


runner = make_runner("paren.tm")


@runner(step=2, trials=1)
def accepting_pairs(step: int, trials: int):
    return itertools.chain((length, (["(", ")"] * (length // 2)
                                     for x in range(trials)))
                           for length in itertools.count(step=step))


@runner(step=2, trials=1)
def accepting_nested(step: int, trials: int):
    return itertools.chain((length, (["("] * (length // 2) + [")"] * (length // 2)
                                     for x in range(trials)))
                           for length in itertools.count(step=step))


@runner(step=2, trials=10)
def accepting_random(step: int, trials: int):
    def generate(length: int):
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
    return itertools.chain((length, [generate(length)
                                     for i in range(trials)])
                           for length in itertools.count(step=step))


@runner(step=2, trials=10)
def completely_random(step: int, trials: int):
    def generate(length: int):
        return ["(" if random.randint(0, 1) == 0 else ")" for x in range(length)]
    return itertools.chain((length, [generate(length)
                                     for i in range(trials)])
                           for length in itertools.count(step=step))
