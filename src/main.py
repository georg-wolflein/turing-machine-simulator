import sys
from parsing import parse_machine, SyntaxError
from tm import TuringMachineError

if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2:
            machine = parse_machine(sys.argv[1])
        else:
            print("Missing machine input", file=sys.stderr)
            print("input error")
            exit(2)
        input_word = []
        if len(sys.argv) >= 3:
            with open(sys.argv[2]) as f:
                input_word = list(f.read().replace("\n", "").replace(" ", ""))
        result = machine.process_input(input_word)
        print("accepted" if result.accepted else "not accepted")
        print(result.num_steps)
        print(" ".join(result.tape))
        exit(0 if result.accepted else 1)
    except IOError:
        exit(3)
    except SyntaxError as e:
        print(e.message, file=sys.stderr)
        print("input error")
        exit(2)
    except TuringMachineError as e:
        print(e.message, file=sys.stderr)
        print("input error")
        exit(2)
