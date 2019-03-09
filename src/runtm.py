#!/usr/bin/env python3

'''Main program entry.
'''

import sys
import typing
from turing.parsing import parse_machine
from turing.error import ExecutionError


def fail(code: int, message: str, error: typing.Union[Exception, str]):
    '''Convenience function for printing failure messages.

    Arguments:
        code {int} -- the exit code
        message {str} -- the message
        error {typing.Union[Exception, str]} -- the exception or message
    '''

    print(error, file=sys.stderr)
    print(message)
    exit(code)


def read_input_word(filename: str) -> list:
    '''Reads the input word from a file.

    Arguments:
        filename {str} -- the name of the file

    Returns:
        list -- the tape input
    '''

    try:
        with open(filename) as f:
            return list(f.read().replace("\n", "").replace(" ", ""))
    except IOError as e:
        fail(3, "tape could not be opened", e)


if __name__ == "__main__":
    args = sys.argv[1::]

    # determine if -v and -n flags are set
    verbose, deterministic = False, True
    while len(args) > 0 and args[0] in ("-n", "-v"):
        if args[0] == "-n":
            deterministic = False
        if args[0] == "-v":
            verbose = True
        args = args[1:]
    if len(args) == 0:
        fail(3, "input error", "missing machine input")

    # parse machine file and tape word arguments
    machine_file = args[0]
    input_word = read_input_word(args[1]) if len(args) >= 2 else []

    # run the machine
    try:
        machine = parse_machine(machine_file, deterministic=deterministic)
        result = machine.process_input(input_word, verbose=verbose)
        print(str(result))
        exit(0 if result.accepted else 1)
    except IOError:
        fail(3, "input error", "could not access machine description")
    except ExecutionError as e:
        fail(2, "input error", e)
