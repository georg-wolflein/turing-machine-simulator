import sys
from parsing import parse_machine

if __name__ == "__main__":
    machine = parse_machine(sys.argv[1])
    machine.process_input(["a", "a", "a", "b", "a"])
