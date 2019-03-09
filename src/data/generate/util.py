import itertools
import os

from turing.parsing import parse_machine

from data import DATA_DIR

NUM_ITERATIONS = 500


def make_runner(*tm_files: str):
    machines = [(tm_file, parse_machine(tm_file)) for tm_file in tm_files]

    def decorator(trials: int, description: str, step: int = 1, iterations: int = NUM_ITERATIONS):
        def runner(func):
            if not os.path.isdir(DATA_DIR):
                os.makedirs(DATA_DIR)
            for tm_file, machine in machines:
                tm = os.path.splitext(os.path.basename(tm_file))[0]
                filename = os.path.join(
                    DATA_DIR, "{}-{}.csv".format(os.path.basename(tm), func.__name__))
                print("Generating {}...".format(filename))
                with open(filename, "w", buffering=1) as f:
                    f.write(r"# Result of running $M_\text{}$ \\ on {} \\ for {} trial{}".format(
                        "{" + tm.replace("_", "\\_") + "}", description, trials, "" if trials == 1 else "s"))
                    f.write("\nn,num_steps\n")
                    for length in itertools.islice(itertools.count(step=step), iterations):
                        for _ in range(trials):
                            tape = func(length)
                            f.write("{},{}\n".format(
                                len(tape), machine.process_input(tape).num_steps))
        return runner
    return decorator
