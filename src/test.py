import optimisations
import numpy as np

tape = np.array([0, 4, 2, 3, 4], dtype="uint16")
print(optimisations.read_state(tape))

print(optimisations.apply_transition(tape, 3, 1, True))
print(optimisations.apply_transition(tape, 3, 1, True))
if optimisations.apply_transition(tape, 3, 1, True):
    tape.resize(len(tape) * 3, refcheck=False)
print(optimisations.apply_transition(tape, 3, 1, True))
print(optimisations.read_state(tape))
print(tape)
