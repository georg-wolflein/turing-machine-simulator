import typing
import sys
import os
from description import DeterministicTuringMachineDescription
from error import assert_property


class TuringMachineResult:
    def __init__(self, num_steps: int, accepted: bool, tape: typing.List[str]):
        self.num_steps = num_steps
        self.accepted = accepted
        for i, letter in enumerate(reversed(tape)):
            if letter != "_":
                break
        self.tape = tape[:-i] if i > 0 else tape
        if self.tape == []:
            self.tape = ["_"]

    def __str__(self):
        return ("accepted" if self.accepted else "not accepted") + os.linesep + str(self.num_steps) + os.linesep + "".join(self.tape)


class TuringMachineConfiguration:
    def __init__(self, current: str, tape: list, position: int = 0, is_accepting: bool = False, is_rejecting: bool = False):
        self.current = current
        self.tape = tape
        self.position = position
        self.is_accepting = is_accepting
        self.is_rejecting = is_rejecting

    def is_terminating(self):
        return self.is_accepting or self.is_rejecting

    def print(self):
        print(" {:5s} ".format(self.current), end="")
        for i, letter in enumerate(self.tape):
            if i == self.position:
                print('\033[91m', end="")
            print(letter, end=" ")
            if i == self.position:
                print('\033[0m', end="")
        print()


class TuringMachine:

    def __init__(self, description: DeterministicTuringMachineDescription):
        self.description = description

    def process_input(self, input: list, verbose: bool = False) -> TuringMachineResult:
        assert_property(all(x in self.description.alphabet or x == "_" for x in input),
                        "input contains invalid characters")
        configuration = TuringMachineConfiguration(
            self.description.initial, input)
        num_steps = 0
        if verbose:
            configuration.print()
        while True:
            configuration = self.perform_step(configuration)
            if verbose:
                configuration.print()
            if configuration.is_terminating():
                break
            else:
                num_steps += 1
        return TuringMachineResult(num_steps, configuration.is_accepting, configuration.tape)

    def go_to_state(self, configuration: TuringMachineConfiguration, state: str, ):
        assert state in self.description.states
        configuration.current = state
        configuration.is_accepting = configuration.current == self.description.accepting
        configuration.is_rejecting = configuration.current == self.description.rejecting

    def read(self, configuration: TuringMachineConfiguration) -> str:
        if configuration.position == 0 and len(configuration.tape) == 0:
            configuration.tape.append("_")
        assert configuration.position >= 0 and configuration.position < len(
            configuration.tape)
        return configuration.tape[configuration.position]

    def write(self, configuration: TuringMachineConfiguration, letter: str):
        assert configuration.position >= 0 and configuration.position < len(
            configuration.tape)
        assert_property(letter in self.description.alphabet or letter ==
                        "_", "letter to be written is not a tape symbol")
        configuration.tape[configuration.position] = letter

    def move_head(self, configuration: TuringMachineConfiguration, right: bool):
        if right:
            configuration.position += 1
        elif configuration.position > 0:
            configuration.position -= 1
        if len(configuration.tape) == configuration.position:
            configuration.tape.append("_")

    def perform_step(self, configuration: TuringMachineConfiguration) -> TuringMachineConfiguration:
        head = self.read(configuration)
        current = self.description.states[configuration.current]
        if head in current:
            to_state, tape_output, move_right = current[head]
            self.write(configuration, tape_output)
            self.move_head(configuration, move_right)
            self.go_to_state(configuration, to_state)
        else:
            self.move_head(configuration, False)
            self.go_to_state(configuration, self.description.rejecting)
        return configuration
