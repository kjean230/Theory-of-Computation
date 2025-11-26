from DPDA_FILE import *

class DPDA: # holds the machine state, transitions, and run logic
    def __init__(self):
        self.transitions = TRANSITIONS
        self.state = None
        self.idc = 0
        self.input_str = ""
        self.stack = []
        self.trace = []

    def normalize_input(self, x):
        ...