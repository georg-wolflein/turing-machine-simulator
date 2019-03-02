import numpy as np
cimport numpy as np


def apply_transition(unsigned long[:] arr):
    pass

ctypedef struct ConfigurationStruct:
    unsigned long position
    unsigned long state
    

# @cython.boundscheck(False) # turn off bounds-checking for entire function
# @cython.wraparound(False)  # turn off negative index wrapping for entire function
# def apply_transition(np.ndarray[LETTERTYPE_t] configuration, unsigned long to_state, unsigned long tape_output, bool move_right):
#     cdef position = 
# 
# @cython.boundscheck(False) # turn off bounds-checking for entire function
# @cython.wraparound(False)  # turn off negative index wrapping for entire function
# def read_letter_and_state(np.ndarray[LETTERTYPE_t] configuration):
