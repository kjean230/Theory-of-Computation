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
        s = "".join(x) if isinstance(x, (list, tuple)) else (x if isinstance(x, str) else None)
        if s is None:
            raise ValueError("Input has to be a string, list, or tuple.")
        s = s.strip()
        if not s.endswith(END):
            s += END
            for ch in s:
                if ch not in SIGMA:
                    raise ValueError(f"Illegal symbol: {repr(ch)}; allowed symbols: {SIGMA}")
        return s
    
    def reset(self, s):
        self.input_str = s 
        self.idx = 0
        self.state = P
        self.stack = []
        self.trace = []