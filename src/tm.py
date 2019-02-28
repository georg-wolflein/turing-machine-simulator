import typing
import sys


class ExecutionError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class TuringMachineError(ExecutionError):
    def __init__(self, message: str):
        super().__init__(message)


def assert_property(cond: bool, message: str):
    if not cond:
        raise TuringMachineError(message)


class TuringMachineDescription:
    def __init__(self):
        self.alphabet = set()
        self.states = dict()
        self.initial = None
        self.accepting = None
        self.rejecting = None

    def add_letter(self, letter: str):
        assert_property(letter not in self.alphabet,
                        "letter is already defined")
        assert_property(letter != "_", "the _ letter is reserved")
        self.alphabet.add(letter)

    def add_state(self, state: str):
        assert_property(state not in self.states, "state is already defined")
        self.states[state] = dict()

    def set_initial(self, state: str):
        assert_property(state in self.states,
                        "initial state is not yet defined")
        self.initial = state

    def set_accepting(self, state: str):
        assert_property(self.accepting == None,
                        "accept state is already defined")
        assert_property(state in self.states,
                        "accept state is not yet defined")
        assert_property(state != self.rejecting,
                        "accept and reject states must be different")
        self.accepting = state

    def set_rejecting(self, state: str):
        assert_property(self.rejecting == None,
                        "reject state is already defined")
        assert_property(state in self.states,
                        "reject state is not yet defined")
        assert_property(state != self.accepting,
                        "accept and reject states must be different")
        self.rejecting = state

    def add_transition(self, from_state: str, tape_input: str, to_state: str, tape_output: str, move_right: bool):
        assert_property(from_state in self.states,
                        "from state {} is not a valid state".format(from_state))
        assert_property(to_state in self.states,
                        "to state {} is not a valid state".format(to_state))
        assert_property(from_state not in (self.accepting, self.rejecting),
                        "the accept and reject states may not have outgoing transitions")
        assert_property(
            tape_input not in self.states[from_state], "transitions cannot be defined multiple times")
        assert_property(tape_input in self.alphabet or tape_input ==
                        "_", "tape input must be in the alphabet")
        assert_property(tape_output in self.alphabet or tape_output ==
                        "_", "tape output must be in alphabet")

        self.states[from_state][tape_input] = (
            to_state, tape_output, move_right)

    def verify_validity(self):
        assert_property(self.accepting != None, "accept state must be defined")
        assert_property(self.rejecting != None, "reject state must be defined")
        assert_property(self.initial != None, "initial state must be defined")


class TuringMachineResult:
    def __init__(self, num_steps: int, accepted: bool, tape: typing.List[str]):
        self.num_steps = num_steps
        self.accepted = accepted
        for i, letter in enumerate(reversed(tape)):
            if letter != "_":
                break
        self.tape = tape[:-i]
        if self.tape == []:
            self.tape = ["_"]


class TuringMachine:

    def __init__(self, description: TuringMachineDescription):
        description.verify_validity()
        self.alphabet = description.alphabet
        self.states = description.states
        self.initial = description.initial
        self.accepting = description.accepting
        self.rejecting = description.rejecting
        self.current = self.initial

    def print_state(self):
        print(" {:5s} ".format(self.current), end="")
        for i, letter in enumerate(self.tape):
            if i == self.position:
                print('\033[91m', end="")
            print(letter, end=" ")
            if i == self.position:
                print('\033[0m', end="")
        print()

    def process_input(self, input: list, verbose: bool = False) -> TuringMachineResult:
        assert_property(all(x in self.alphabet or x == "_" for x in input),
                        "input contains invalid characters")
        self.tape = input
        self.position = 0
        self.has_accepted = False
        self.has_rejected = False
        num_steps = 0
        if verbose:
            self.print_state()
        while True:
            self.perform_next_step()
            if verbose:
                self.print_state()
            if self.has_terminated():
                break
            else:
                num_steps += 1
        return TuringMachineResult(num_steps, self.has_accepted, self.tape)

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

    def perform_next_step(self):
        head = self.read()
        current = self.get_current_state()
        if head in current:
            to_state, tape_output, move_right = current[head]
            self.write(tape_output)
            self.move_head(move_right)
            self.go_to_state(to_state)
        else:
            self.move_head(False)
            self.go_to_state(self.rejecting)

    def has_terminated(self) -> bool:
        return self.has_accepted or self.has_rejected
