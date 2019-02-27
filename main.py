from tm import TuringMachine, TuringMachineDescription
import sys


class SyntaxError(Exception):
    def __init__(self, message: str):
        self.message = message


def assert_syntax(cond: bool, message: str):
    if not cond:
        raise SyntaxError(message)


def assert_cast(var, t: type, message: str):
    try:
        return t(var)
    except ValueError:
        raise SyntaxError(message)


def create_turing_machine(encoded_machine_file: str) -> TuringMachine:
    with open(encoded_machine_file, "r") as f:
        description = TuringMachineDescription()

        # states heading
        line = f.readline().strip().split(" ")
        assert_syntax(len(line) == 2, "states heading not properly defined")
        states_str, num_states = line
        assert_syntax(states_str == "states",
                      "expected states heading, got {}".format(states_str))
        num_states = assert_cast(
            num_states, int, "the number of states must be an integer")

        # process states
        for i in range(num_states):
            line = f.readline().strip().split(" ")
            assert_syntax(len(line) <= 2,
                          "too many arguments to define the state")
            state_name = line[0]
            description.add_state(state_name)
            if len(line) == 2:
                accept_or_reject = line[1]
                assert_syntax(accept_or_reject in ("+", "-"),
                              "second argument must be + or -")
                if accept_or_reject == "+":
                    description.set_accepting(state_name)
                else:
                    description.set_rejecting(state_name)
            if i == 0:
                description.set_initial(state_name)

        # process alphabet
        line = f.readline().strip().split(" ")
        assert_syntax(len(line) >= 2, "too few arguments to define alphabet")
        assert_syntax(line[0] == "alphabet", "expected alphabet heading")
        num_letters = assert_cast(
            line[1], int, "the number of letters in the alphabet must be an integer")
        alphabet = line[2::]
        assert_syntax(len(alphabet) == num_letters,
                      "the actual number of letters needs to match the number of letters provided")
        for letter in alphabet:
            description.add_letter(letter)

        while True:
            line = f.readline().strip()
            if not line:
                break
            line = line.split(" ")
            assert_syntax(len(line) == 5, "the line requires five arguments")
            from_state, tape_input, to_state, tape_output, action = line
            assert_syntax(action in ["L", "R"],
                          "the action must either be L or R")
            move_right = action == "R"
            description.add_transition(
                from_state, tape_input, to_state, tape_output, move_right)
        return TuringMachine(description)


if __name__ == "__main__":
    machine = create_turing_machine(sys.argv[1])
    machine.process_input(["a", "a", "a", "b"])
