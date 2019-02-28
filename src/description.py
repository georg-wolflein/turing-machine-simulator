from abc import ABC, abstractmethod
from error import assert_property


class TuringMachineDescription(ABC):
    def __init__(self):
        self.alphabet = set()
        self.states = dict()
        self.initial = None
        self.accepting = None
        self.rejecting = None

    @abstractmethod
    def add_letter(self, letter: str):
        assert_property(letter not in self.alphabet,
                        "letter is already defined")
        assert_property(letter != "_", "the _ letter is reserved")

    @abstractmethod
    def add_state(self, state: str):
        assert_property(state not in self.states, "state is already defined")

    @abstractmethod
    def set_initial(self, state: str):
        assert_property(state in self.states,
                        "initial state is not yet defined")

    @abstractmethod
    def set_accepting(self, state: str):
        assert_property(self.accepting == None,
                        "accept state is already defined")
        assert_property(state in self.states,
                        "accept state is not yet defined")
        assert_property(state != self.rejecting,
                        "accept and reject states must be different")

    @abstractmethod
    def set_rejecting(self, state: str):
        assert_property(self.rejecting == None,
                        "reject state is already defined")
        assert_property(state in self.states,
                        "reject state is not yet defined")
        assert_property(state != self.accepting,
                        "accept and reject states must be different")

    @abstractmethod
    def add_transition(self, from_state: str, tape_input: str, to_state: str, tape_output: str, move_right: bool):
        assert_property(from_state in self.states,
                        "from state {} is not a valid state".format(from_state))
        assert_property(to_state in self.states,
                        "to state {} is not a valid state".format(to_state))
        assert_property(from_state not in (self.accepting, self.rejecting),
                        "the accept and reject states may not have outgoing transitions")
        assert_property(tape_input in self.alphabet or tape_input ==
                        "_", "tape input must be in the alphabet")
        assert_property(tape_output in self.alphabet or tape_output ==
                        "_", "tape output must be in alphabet")

    def verify_validity(self):
        assert_property(self.accepting != None, "accept state must be defined")
        assert_property(self.rejecting != None, "reject state must be defined")
        assert_property(self.initial != None, "initial state must be defined")


class DeterministicTuringMachineDescription(TuringMachineDescription):
    def __init__(self):
        super().__init__()

    def add_letter(self, letter: str):
        super().add_letter(letter)
        self.alphabet.add(letter)

    def add_state(self, state: str):
        super().add_state(state)
        self.states[state] = dict()

    def set_initial(self, state: str):
        super().set_initial(state)
        self.initial = state

    def set_accepting(self, state: str):
        super().set_accepting(state)
        self.accepting = state

    def set_rejecting(self, state: str):
        super().set_rejecting(state)
        self.rejecting = state

    def add_transition(self, from_state: str, tape_input: str, to_state: str, tape_output: str, move_right: bool):
        super().add_transition(from_state, tape_input, to_state, tape_output, move_right)
        assert_property(
            tape_input not in self.states[from_state], "transitions cannot be defined multiple times")
        self.states[from_state][tape_input] = (
            to_state, tape_output, move_right)


class NondeterministicTuringMachineDescription(TuringMachineDescription):
    def __init__(self):
        super().__init__()

    def add_letter(self, letter: str):
        super().add_letter(letter)
        self.alphabet.add(letter)

    def add_state(self, state: str):
        super().add_state(state)
        self.states[state] = dict()

    def set_initial(self, state: str):
        super().set_initial(state)
        self.initial = state

    def set_accepting(self, state: str):
        super().set_accepting(state)
        self.accepting = state

    def set_rejecting(self, state: str):
        super().set_rejecting(state)
        self.rejecting = state

    def add_transition(self, from_state: str, tape_input: str, to_state: str, tape_output: str, move_right: bool):
        super().add_transition(from_state, tape_input, to_state, tape_output, move_right)
        if tape_input not in self.states[from_state]:
            self.states[from_state][tape_input] = list()
        self.states[from_state][tape_input].append(
            (to_state, tape_output, move_right))
