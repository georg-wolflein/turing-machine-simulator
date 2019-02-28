import typing
import sys
import os
from description import DeterministicTuringMachineDescription, NondeterministicTuringMachineDescription, TuringMachineDescription
from error import assert_property
from abc import ABC, abstractmethod


class TuringMachineResult:
    def __init__(self, num_steps: int, accepted: bool, tape: typing.Union[typing.List[str], None]):
        self.num_steps = num_steps
        self.accepted = accepted
        if tape is None:
            self.tape = None
        else:
            for i, letter in enumerate(reversed(tape)):
                if letter != "_":
                    break
            self.tape = tape[:-i] if i > 0 else tape
            if self.tape == []:
                self.tape = ["_"]

    def __str__(self):
        return ("accepted" if self.accepted else "not accepted") + os.linesep + str(self.num_steps) + ((os.linesep + "".join(self.tape)) if self.tape is not None else "")


class TuringMachineConfiguration:
    def __init__(self, current: str, tape: list, position: int = 0):
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

    def duplicate(self):
        return TuringMachineConfiguration(self.current, self.tape[::], self.position)

    def print(self):
        print(" {:5s} ".format(self.current), end="")
        for i, letter in enumerate(self.tape):
            if i == self.position:
                print('\033[91m', end="")
            print(letter, end=" ")
            if i == self.position:
                print('\033[0m', end="")
            if i > 100:
                break
        print()

    def __hash__(self):
        return hash((self.current, self.position) + tuple(self.tape))

    def __eq__(self, other):
        if not isinstance(other, TuringMachineConfiguration):
            return False
        return self.position == other.position and self.current == other.current and self.tape == other.tape


class TuringMachine(ABC):
    def __init__(self, description: TuringMachineDescription):
        self.description = description

    def is_terminating(self, configuration: TuringMachineConfiguration) -> bool:
        return configuration.current in (self.description.accepting, self.description.rejecting)

    @abstractmethod
    def process_input(self, input: list, verbose: bool = False) -> TuringMachineResult:
        assert_property(all(x in self.description.alphabet or x == "_" for x in input),
                        "input contains invalid characters")


class DeterministicTuringMachine(TuringMachine):

    def __init__(self, description: DeterministicTuringMachineDescription):
        super().__init__(description)

    def process_input(self, input: list, verbose: bool = False) -> TuringMachineResult:
        super().process_input(input, verbose)
        configuration = TuringMachineConfiguration(
            self.description.initial, input)
        num_steps = 0
        if verbose:
            configuration.print()
        while True:
            self.perform_step(configuration)
            if verbose:
                configuration.print()
            if self.is_terminating(configuration):
                break
            else:
                num_steps += 1
            input()
        return TuringMachineResult(num_steps, configuration.current == self.description.accepting, configuration.tape)

    def perform_step(self, configuration: TuringMachineConfiguration):
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


class NondeterministicTuringMachine(TuringMachine):
    def __init__(self, description: NondeterministicTuringMachineDescription):
        super().__init__(description)

    def process_input(self, input: list, verbose: bool = False) -> TuringMachineResult:
        super().process_input(input, verbose)
        configurations = set([TuringMachineConfiguration(
            self.description.initial, input)])
        num_steps = 0

        if verbose:
            for configuration in configurations:
                configuration.print()
            print()

        while True:
            # filter out configurations that reject
            nonrejecting_configurations = set()
            for configuration in configurations:
                for possibility in self.perform_step(configuration):
                    if possibility.current == self.description.accepting:
                        # if we have an accepting configuration, accept
                        return TuringMachineResult(num_steps, True, None)
                    elif configuration.current != self.description.rejecting:
                        nonrejecting_configurations.add(possibility)
            configurations = nonrejecting_configurations
            # reject if there are no configurations left
            if len(configurations) == 0:
                return TuringMachineResult(num_steps, False, None)
            if verbose:
                for configuration in configurations:
                    configuration.print()
                print()
            num_steps += 1

    def perform_step(self, configuration: TuringMachineConfiguration) -> typing.List[TuringMachineConfiguration]:
        head = configuration.read()
        current = self.description.states[configuration.current]
        if head in current:
            transitions = current[head]
            confs = []
            for i, (to_state, tape_output, move_right) in enumerate(transitions):
                # skip duplicating last transition
                if i == len(transitions) - 1:
                    conf = configuration
                else:
                    conf = configuration.duplicate()
                conf.write(tape_output)
                conf.move_head(move_right)
                conf.go_to_state(to_state)
                confs.append(conf)
            return confs
        else:
            return []
