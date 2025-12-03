# DPDA_class.py — DPDA engine, trace printing, and CLI
from DPDA_FILE import (
    EPS, END, BOT,
    P, Q, QA, QB, QD, QACC,
    FINAL_STATES, SIGMA, TABLE_HEADER, TRANSITIONS
)

class DPDA:
    def __init__(self):
        self.transitions = TRANSITIONS
        self.state = None
        self.idx = 0
        self.input_str = ""
        self.stack = []    # Python list; rightmost element is the TOP
        self.trace = []    # rows of (step, state, unread, top, Δ, G)

    def normalize_input(self, x):
        s = "".join(x) if isinstance(x, (list, tuple)) else (x if isinstance(x, str) else None)
        if s is None:
            raise ValueError("Input has to be a string, list, or tuple.")
        s = s.strip()
        if not s.endswith(END):
            s += END
        # Enforce exactly one trailing '$'
        if s.count(END) != 1 or s[-1] != END:
            raise ValueError("Input must contain exactly one end marker '$' at the end.")
        # Enforce only allowed characters
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
            self._stack_top(),
            label,
            g
        ))

    def _match_entry(self):
        la = self._next_input()
        top = self._stack_top()
        st  = self.state
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

    def _apply(self, entry):
        (_, in_sym, top_sym, next_state, push, _label, _g, consumes) = entry
        if top_sym != EPS and self.stack:
            self.stack.pop()           # pop expected top
        for ch in push:
            self.stack.append(ch)      # push left→right; rightmost becomes top
        if consumes:
            self.idx += 1              # advance input
        self.state = next_state

    def run(self, input_obj):
        s = self.normalize_input(input_obj)
        self.reset(s)
        step = 0
        while True:
            if self.state in FINAL_STATES:
                # As normalize_input enforces exactly one trailing '$',
                # reaching q_accept implies full consumption.
                return True, self.trace

            entry = self._match_entry()
            if entry is None:
                self._append_row(step, "—", "—")
                return False, self.trace

            _s, in_sym, _t, _n, _push, label, g, _c = entry
            self._append_row(step, label, g)
            self._apply(entry)
            step += 1

    def print_table(self):
        print(TABLE_HEADER)
        for step, state, unread, top, label, g in self.trace:
            print(f"{step:>4} | {state:<4} | {unread:<12} | {top:^3} | {label:<36} | {g}")

    @staticmethod
    def main():
        import argparse, sys
        ap = argparse.ArgumentParser(
            description="DPDA for L = { a^n b^n } with one-symbol lookahead and end-marker '$'"
        )
        ap.add_argument("inputs", nargs="*", help="Inputs like ab$, aabb$ (program appends '$' if missing).")
        ap.add_argument("--all", action="store_true",
                        help="Run demo suite: $, ab$, aabb$, aaabbb$, aaaabbbb$, aaaaaabbbbbb$.")
        args = ap.parse_args()

        # Interactive fallback
        if not args.inputs and not args.all:
            raw = input("Enter one or more inputs (comma-separated), or 'q' to quit: ").strip()
            if raw.lower() in {"q", "quit", "exit"}:
                sys.exit(0)
            args.inputs = [part.strip() for part in raw.split(",") if part.strip()]

        suite = args.inputs if args.inputs else (
            ["$", "ab$", "aabb$", "aaabbb$", "aaaabbbb$", "aaaaaabbbbbb$"] if args.all else []
        )
        if not suite:
            ap.print_usage()
            print("\nProvide inputs (e.g., `python DPDA_class.py aabb$`) or use `--all`.", file=sys.stderr)
            sys.exit(2)

        overall_ok = True
        for s in suite:
            m = DPDA()
            try:
                ok, _rows = m.run(s)
            except ValueError as e:
                overall_ok = False
                print(f"\nInput: {s}\nERROR: {e}")
                continue

            print(f"\nInput: {s}  →  {'ACCEPT' if ok else 'REJECT'}")
            m.print_table()
            if not ok:
                overall_ok = False

        sys.exit(0 if overall_ok else 1)


if __name__ == "__main__":
    DPDA.main()