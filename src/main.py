import sys
import typing
from parsing import parse_machine
from tm import ExecutionError


def fail(code: int, message: str, error: typing.Union[Exception, str]):
    print(error, file=sys.stderr)
    print(message)
    exit(code)


def read_input_word(filename: str) -> list:
    try:
        with open(filename) as f:
            return list(f.read().replace("\n", "").replace(" ", ""))
    except IOError as e:
        fail(3, "tape could not be opened", e)


if __name__ == "__main__":
    args = sys.argv[1::]
    verbose, nondeterministic = False, False
    while len(args) > 0 and args[0] in ("-n", "-v"):
        if args[0] == "-n":
            nondeterministic = True
        if args[0] == "-v":
            verbose = True
        args = args[1:]
    if len(args) == 0:
        fail(3, "input error", "missing machine input")

    machine_file = args[0]
    input_word = read_input_word(args[1]) if len(args) >= 2 else []

    try:
        machine = parse_machine(machine_file)
        result = machine.process_input(input_word, verbose=verbose)
        print("accepted" if result.accepted else "not accepted")
        print(result.num_steps)
        print(" ".join(result.tape))
        exit(0 if result.accepted else 1)
    except IOError:
        fail(3, "input error", "could not access machine description")
    except ExecutionError as e:
        fail(2, "input error", e)
