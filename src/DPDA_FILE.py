# DPDA_FILE.py (deterministic pushdown automata file operations)
# dpda.py — DPDA for L = { a^n b^n } with one-symbol lookahead

# Special Symbols
EPS = 'ε' # this represents the empty string (EPSILON) - no input
BOT = '⊥' # this represents the bottom stack symbol
P = 'p' # the pre-initial state (before pushing any inputs)
Q = 'q' # the driver state (dispatches lookahead)
QA = 'qa' # the accepting state (if next input symbol is 'a')
QB = 'qb' # the accepting state (if next input symbol is 'b')
QD = 'q$' # when the next input symbol is the endmarker '$'
QACC = "q_accept" # the final accepting state 