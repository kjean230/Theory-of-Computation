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

    def run(self, input_obj):  # execute the DPDA on the given input; return (accepted, trace_rows)
        s = self.normalize_input(input_obj)  # ensure string ends with '$' and uses only allowed symbols
        self.reset(s)                        # start fresh: state=p, idx=0, empty stack, clear trace

        step = 0
        while True:
            if self.state in FINAL_STATES:           # reached accepting state
                return True, self.trace

            entry = self._match_entry()              # pick the single deterministic next move
            if entry is None:                        # no move ⇒ reject with trace as-is
                self._append_row(step, "—", "—")     # log a terminal row showing no applicable transition
                return False, self.trace

            _s, in_sym, _t, _n, _push, label, g, _c = entry
            self._append_row(step, label, g)        # log BEFORE applying the transition (as required by your table)
            self._apply(entry)                       # mutate state, stack, and input index
            step += 1                                # next row number

    def print_table(self):  # print the fixed-width table for the current trace
        print(TABLE_HEADER)
        for step, state, unread, top, label, g in self.trace:
            print(f"{step:>4} | {state:<4} | {unread:<12} | {top:^3} | {label:<36} | {g}")
