import itertools
import os

from turing.parsing import parse_machine

OUTPUT_DIR = "data_out"
NUM_ITERATIONS = 500
PRINT_INTERVAL = 100


def avg(x: list):
    return sum(x) / len(x)


def make_runner(tm_file: str):
    machine = parse_machine(tm_file)

    def decorator(step: int, trials: int):
        def runner(func):
            if not os.path.isdir(OUTPUT_DIR):
                os.makedirs(OUTPUT_DIR)
            filename = os.path.join(
                OUTPUT_DIR, "{}-{}.csv".format(os.path.basename(tm_file), func.__name__))
            print("Generating {}...".format(filename))
            with open(filename, "w") as f:
                f.write("# {}: (step={}, trials={})\n".format(
                    func.__name__, step, trials))
                f.write("# n, avg(num_steps)\n")
                for i, (n, tapes) in enumerate(itertools.islice(func(step, trials), 500)):
                    if i % PRINT_INTERVAL == 0:
                        print("  iteration {} out of {}".format(
                            i, NUM_ITERATIONS))
                    f.write("{},{}\n".format(
                        n, avg([machine.process_input(tape).num_steps for tape in tapes])))
        return runner
    return decorator
