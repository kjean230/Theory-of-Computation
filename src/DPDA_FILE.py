# DPDA_FILE.py (deterministic pushdown automata file operations)
# dpda.py — DPDA for L = { a^n b^n } with one-symbol lookahead

# Special Symbols
EPS = 'ε' # this represents the empty string (EPSILON) - no input
BOT = '⊥' # this represents the bottom stack symbol
END = '$' # the input endmarker symbol

P = 'p' # the pre-initial state (before pushing any inputs)
Q = 'q' # the driver state (dispatches lookahead)
QA = 'qa' # the accepting state (if next input symbol is 'a')
QB = 'qb' # the accepting state (if next input symbol is 'b')
QD = 'q$' # when the next input symbol is the endmarker '$'
QACC = "q_accept" # the final accepting state 

STATES = {P, Q, QA, QB, QD, QACC} # complete states that the DPDA can be in 
FINAL_STATES = {QACC} # the ONLY final accepting state

SIGMA = {"a", "b", END} # input alphabet (including endmarker '$')
GAMMA = {"S", "a", "b", BOT} # the symbols that are allowed within the stack

G1 = "S→aSb" # the first grammer rule when expanding 'S'
G2 = "S→ε"  # the second grammer rule when expanding 'S' to empty string
