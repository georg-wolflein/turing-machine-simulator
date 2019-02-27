import typing
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


class TuringMachine:

    def __init__(self, alphabet: set, states: set, initial: str, accepting: str, rejecting: str):
        assert_syntax(accepting != rejecting,
                      "accept and reject states must be different")
        self.alphabet = alphabet
        self.states = dict({state: dict() for state in states})
        self.initial = initial
        self.accepting = accepting
        self.rejecting = rejecting
        self.current = self.initial

    def add_transition(self, from_state: str, tape_input: str, to_state: str, tape_output: str, move_right: bool):
        assert_syntax(from_state in self.states,
                      "from state must be a valid state")
        assert_syntax(to_state in self.states,
                      "to state must be a valid state")
        assert_syntax(from_state not in (self.accepting, self.rejecting),
                      "the accept and reject states may not have outgoing transitions")
        assert_syntax(
            tape_input not in self.states[from_state], "transitions cannot be defined multiple times")
        # assert tape_input in self.alphabet
        # assert tape_output in self.alphabet

        self.states[from_state][tape_input] = (
            to_state, tape_output, move_right)

    def process_input(self, input: list):
        assert_syntax(all(x in self.alphabet for x in input),
                      "input contains invalid characters")
        self.tape = input
        self.position = 0
        self.has_accepted = False
        self.has_rejected = False
        while not self.has_terminated():
            self.perform_next_step()
            print(" ".join(self.tape[0:self.position]), end="")
            print("(" + self.read() + ")", end="")
            print(" ".join(self.tape[self.position+1:]))
        if self.has_accepted:
            print("Accepted")
        if self.has_rejected:
            print("Rejected")

    def get_current_state(self):
        return self.states[self.current]

    def go_to_state(self, state: str):
        assert state in self.states
        self.current = state
        if self.current == self.accepting:
            self.has_accepted = True
        if self.current == self.rejecting:
            self.has_rejected = True

    def read(self) -> str:
        if self.position == 0 and len(self.tape) == 0:
            self.tape.append("_")
        assert self.position >= 0 and self.position < len(self.tape)
        return self.tape[self.position]

    def write(self, letter: str):
        assert self.position >= 0 and self.position < len(self.tape)
        # assert letter in self.alphabet
        self.tape[self.position] = letter

    def move_head(self, right: bool):
        if right:
            self.position += 1
        elif self.position > 0:
            self.position -= 1
        if len(self.tape) == self.position:
            self.tape.append("_")

    def perform_next_step(self) -> bool:
        head = self.read()
        current = self.get_current_state()
        assert head in current
        to_state, tape_output, move_right = current[head]
        self.write(tape_output)
        self.move_head(move_right)
        self.go_to_state(to_state)

    def has_terminated(self) -> bool:
        return self.has_accepted or self.has_rejected


def create_turing_machine(encoded_machine_file: str) -> TuringMachine:
    with open(encoded_machine_file, "r") as f:
        states = set()
        initial, accepting, rejecting = None, None, None
        alphabet = None

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
            assert_syntax(state_name not in states,
                          "state has already been defined")
            states.add(state_name)
            if len(line) == 2:
                accept_or_reject = line[1]
                assert_syntax(accept_or_reject in ("+", "-"),
                              "second argument must be + or -")
                if accept_or_reject == "+":
                    assert_syntax(accepting is None,
                                  "you cannot define two accepting states")
                    accepting = state_name
                else:
                    assert_syntax(rejecting is None,
                                  "you cannot define two rejecting states")
                    rejecting = state_name
            if i == 0:
                initial = state_name

        # process alphabet
        line = f.readline().strip().split(" ")
        assert_syntax(len(line) >= 2, "too few arguments to define alphabet")
        assert_syntax(line[0] == "alphabet", "expected alphabet heading")
        num_letters = assert_cast(
            line[1], int, "the number of letters in the alphabet must be an integer")
        alphabet = line[2::]
        assert_syntax(len(alphabet) == num_letters,
                      "the actual number of letters needs to match the number of letters provided")

        machine = TuringMachine(
            alphabet, states, initial, accepting, rejecting)

        while True:
            line = f.readline().strip()
            if not line:
                break
            line = line.split(" ")
            assert_syntax(len(line) == 5, "the line requires five arguments")
            from_state, tape_input, to_state, tape_output, action = line
            # assert from_state in states
            # assert to_state in states
            # assert tape_input in alphabet
            # assert tape_output in alphabet
            assert_syntax(action in ["L", "R"],
                          "the action must either be L or R")
            move_right = action == "R"
            machine.add_transition(
                from_state, tape_input, to_state, tape_output, move_right)
        return machine


if __name__ == "__main__":
    machine = create_turing_machine(sys.argv[1])
    machine.process_input(["a", "a", "a", "b"])
