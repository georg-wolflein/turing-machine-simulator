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

    def go_to_state(self, state: str):
        self.current = state

    def read(self) -> str:
        if self.position == 0 and len(self.tape) == 0:
            self.tape.append("_")
        return self.tape[self.position]

    def write(self, letter: str):
        self.tape[self.position] = letter

    def move_head(self, right: bool):
        if right:
            self.position += 1
        elif self.position > 0:
            self.position -= 1
        if len(self.tape) == self.position:
            self.tape.append("_")

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
            if configuration.current in (self.description.accepting, self.description.rejecting):
                break
            else:
                num_steps += 1
        return TuringMachineResult(num_steps, configuration.current == self.description.accepting, configuration.tape)

    def perform_step(self, configuration: TuringMachineConfiguration) -> TuringMachineConfiguration:
        head = configuration.read()
        current = self.description.states[configuration.current]
        if head in current:
            to_state, tape_output, move_right = current[head]
            configuration.write(tape_output)
            configuration.move_head(move_right)
            configuration.go_to_state(to_state)
        else:
            configuration.move_head(False)
            configuration.go_to_state(self.description.rejecting)
        return configuration
