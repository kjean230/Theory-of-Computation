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

    def _stack_top(self):
        return self.stack[-1] if self.stack else EPS
    
    def _unread(self):
        return self.input_str[self.idx:]
    
    def _next_input(self):
        return self.input_str[self.idx] if self.idx < len(self.input_str) else EPS

    def _append_row(self, step, label, g):
        self.trace.append((
            step,
            self.state,
            self._unread(),
            self.stack_top(),
            label,
            g
        ))

    def _match_entry(self):
        la = self._next_input()
        top = self._stack_top()
        st = self.state

        for (s, in_sym, t, next_state, push, label, g, consumes) in self.transitions:
            if s != st:
                continue
            if in_sym == EPS:
                if t == top: 
                    return (s, in_sym, t, next_state, push, label, g, consumes)
            else: 
                if in_sym == la and t == top:
                    return (s, in_sym, t, next_state, push, label, g, consumes)
        return None
    
    def _apply(self, entry):  # execute the selected transition: pop/push stack, advance input, change state
        (_, in_sym, top_sym, next_state, push, _label, _g, consumes) = entry
        if top_sym != EPS and self.stack:  # pop the expected top (if any)
            self.stack.pop()
        for ch in push:                     # push left→right so the rightmost becomes the new top
            self.stack.append(ch)
        if consumes:                        # advance input index if this rule consumes a symbol
            self.idx += 1
        self.state = next_state             # move to the next state
