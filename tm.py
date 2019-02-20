import typing
import sys


class TuringMachine:

    def __init__(self, alphabet: set, states: set, initial: str, accepting: str, rejecting: str):
        assert accepting != rejecting
        self.alphabet = alphabet
        self.states = dict({state: dict() for state in states})
        self.initial = initial
        self.accepting = accepting
        self.rejecting = rejecting
        self.current = self.initial

    def add_transition(self, from_state: str, tape_input: str, to_state: str, tape_output: str, move_right: bool):
        assert from_state in self.states
        assert to_state in self.states
        #assert tape_input in self.alphabet
        #assert tape_output in self.alphabet
        assert from_state not in (self.accepting, self.rejecting)
        assert tape_input not in self.states[from_state]
        self.states[from_state][tape_input] = (
            to_state, tape_output, move_right)

    def process_input(self, input: list):
        # TODO: assert input in alphabet
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
        #assert letter in self.alphabet
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


if __name__ == "__main__":
    encoded_machine_file = sys.argv[1]
    with open(encoded_machine_file, "r") as f:
        states = set()
        initial, accepting, rejecting = None, None, None
        alphabet = None

        # states heading
        line = f.readline().strip().split(" ")
        assert len(line) == 2
        states_str, num_states = line
        assert states_str == "states"
        # -- make sure line[1] is int
        num_states = int(num_states)

        # process states
        for i in range(num_states):
            line = f.readline().strip().split(" ")
            assert len(line) <= 2
            state_name = line[0]
            assert state_name not in states
            states.add(state_name)
            if len(line) == 2:
                accept_or_reject = line[1]
                assert accept_or_reject in ("+", "-")
                if accept_or_reject == "+":
                    assert accepting is None
                    accepting = state_name
                else:
                    assert rejecting is None
                    rejecting = state_name
            if i == 0:
                initial = state_name

        # process alphabet
        line = f.readline().strip().split(" ")
        assert len(line) >= 2
        assert line[0] == "alphabet"
        # -- make sure line[1] is int
        num_letters = int(line[1])
        alphabet = line[2::]
        assert len(alphabet) == num_letters

        machine = TuringMachine(
            alphabet, states, initial, accepting, rejecting)

        while True:
            line = f.readline().strip()
            if not line:
                break
            line = line.split(" ")
            assert len(line) == 5
            from_state, tape_input, to_state, tape_output, action = line
            # assert from_state in states
            # assert to_state in states
            # assert tape_input in alphabet
            # assert tape_output in alphabet
            assert action in ["L", "R"]
            move_right = action == "R"
            machine.add_transition(
                from_state, tape_input, to_state, tape_output, move_right)

        machine.process_input(["a", "a", "a", "b"])
