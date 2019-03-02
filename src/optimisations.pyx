import cython
import numpy as np
cimport numpy as np

ctypedef np.uint16_t DTYPE_t

class Accept(Exception):
    pass

def create_initial_configuration(tape, accepting, rejecting):
    return np.array([0, 0, accepting, rejecting] + [x for x in tape], dtype=np.uint16)

@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False) 
def read_state(unsigned short[:] tape not None):
    return (tape[1], tape[tape[0] + 4])

@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False) 
def apply_transitions(np.ndarray configuration not None, unsigned short[:, :] transitions):
    cdef unsigned short position = configuration[0]
    cdef unsigned short accepting = configuration[2]
    cdef unsigned short rejecting = configuration[3]
    cdef ssize_t I = transitions.shape[0]

    cdef unsigned short to_state
    cdef unsigned short tape_output
    cdef unsigned short move_right
    for i in range(I):
        to_state = transitions[i, 0]
        if to_state == rejecting:
            continue
        if to_state == accepting:
            raise Accept()
        tape_output = transitions[i, 1]
        move_right = transitions[i, 2]
        conf = configuration if i == I - 1 else configuration.copy()
        conf[position + 4] = tape_output
        conf[1] = to_state
        if move_right == 1:
            conf[0] = position + 1
            if conf.shape[0] == position + 5:
                conf.resize(conf.shape[0] * 2, refcheck=False)
        elif position > 0:
            conf[0] = position - 1
        yield conf

# @cython.boundscheck(False) # turn off bounds-checking for entire function
# @cython.wraparound(False) 
# def apply_transition(unsigned short[:] tape not None, unsigned short to_state, unsigned short tape_output, unsigned short move_right):
#     cdef unsigned short position = tape[0]
#     tape[position + 2] = tape_output
#     tape[1] = to_state
#     if move_right:
#         tape[0] = position + 1
#         if tape.shape[0] == position + 3:
#             return True
#     elif position > 0:
#         tape[0] = position - 1
#     return False
    

# @cython.boundscheck(False) # turn off bounds-checking for entire function
# @cython.wraparound(False)  # turn off negative index wrapping for entire function
# def apply_transition(np.ndarray[LETTERTYPE_t] configuration, unsigned short to_state, unsigned short tape_output, bool move_right):
#     cdef position = 
# 
# @cython.boundscheck(False) # turn off bounds-checking for entire function
# @cython.wraparound(False)  # turn off negative index wrapping for entire function
# def read_letter_and_state(np.ndarray[LETTERTYPE_t] configuration):
