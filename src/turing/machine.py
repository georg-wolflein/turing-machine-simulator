import typing
import sys
import itertools
import os
import numpy as np
from abc import ABC, abstractmethod
from turing.description import TuringMachineDescription
from turing.error import assert_property, TuringMachineError
import optimisations


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
    state: int
    tape: np.array
    position: int

    def __init__(self, state: int, tape: np.array, position: int):
        self.state = state
        self.tape = tape
        self.position = position


class DeterministicTuringMachine:

    def __init__(self, description: TuringMachineDescription):
        self.description = description

    def process_input(self, input: list, verbose: bool = False) -> TuringMachineResult:
        if len(input) == 0:
            input = ["_"]
        try:
            tape = np.array([self.description.alphabet.index(x)
                             for x in input], dtype=np.uint8)
        except ValueError:
            raise TuringMachineError("input contains invalid characters")
        configuration = TuringMachineConfiguration(0, tape, 0)
        num_steps = 0
        if verbose:
            self.print_configuration(configuration)
        while True:
            self.perform_step(configuration)
            if verbose:
                self.print_configuration(configuration)
            if configuration.state == self.description.accepting:
                return TuringMachineResult(num_steps, True, [self.description.alphabet[x] for x in configuration.tape])
            if configuration.state == self.description.rejecting:
                return TuringMachineResult(num_steps, False, [self.description.alphabet[x] for x in configuration.tape])
            num_steps += 1

    def perform_step(self, configuration: TuringMachineConfiguration):
        # read
        tape_input = configuration.tape[configuration.position]
        state = self.description.transitions[configuration.state]
        if tape_input in state:
            to_state, tape_output, move_right = state[tape_input]
            # write
            configuration.tape[configuration.position] = tape_output
            # move head
            if move_right:
                configuration.position += 1
                if configuration.position == len(configuration.tape):
                    configuration.tape.resize(
                        configuration.position + 1, refcheck=False)
            elif configuration.position > 0:
                configuration.position -= 1
            # change state
            configuration.state = to_state
        else:
            # move head right
            configuration.position += 1
            # go to rejecting state
            configuration.state = self.description.rejecting

    def print_configuration(self, configuration: TuringMachineConfiguration):
        print(" {:5s} ".format(
            description.states[configuration.state]), end="")
        for i, letter in enumerate(configuration.tape):
            if i == configuration.position:
                print('\033[91m', end="")
            print(description.alphabet[letter], end=" ")
            if i == configuration.position:
                print('\033[0m', end="")
        print()


class NondeterministicTuringMachine:

    class AcceptException(Exception):
        def __init__(self, configuration: TuringMachineConfiguration):
            self.configuration = configuration

    def __init__(self, description: TuringMachineDescription):
        self.description = description

    def process_input(self, input: list, verbose: bool = False) -> TuringMachineResult:
        if len(input) == 0:
            input = ["_"]
        try:
            tape = [self.description.alphabet.index(x) for x in input]
        except ValueError:
            raise TuringMachineError("input contains invalid characters")
        configurations = [optimisations.create_initial_configuration(
            tape, self.description.accepting, self.description.rejecting)]
        num_steps = 0

        def get_next_configurations(configuration):
            state, tape_input = optimisations.read_state(configuration)
            try:
                transitions = self.description.transitions[state][tape_input]
                return optimisations.apply_transitions(configuration, transitions)
            except KeyError:
                return []

        while True:
            if verbose:
                [optimisations.print_configuration(
                    c, self.description.alphabet, self.description.states) for c in configurations]
                print()
            try:
                new_configurations = list(itertools.chain.from_iterable(
                    get_next_configurations(c) for c in configurations))
            except optimisations.Accept:
                return TuringMachineResult(num_steps, True, None)
            configurations = new_configurations
            if len(configurations) == 0:
                return TuringMachineResult(num_steps, False, None)
            num_steps += 1
