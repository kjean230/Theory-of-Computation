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

INIT_PUSH_BOTTOM_AND_START = "init: push ⊥ and S"  # first move: set up the stack with bottom marker and start symbol

LOOKAHEAD_DISPATCH_ON_A = "lookahead a: go to qa"  # if next input is 'a', move to the 'a' gate state
LOOKAHEAD_DISPATCH_ON_B = "lookahead b: go to qb"  # if next input is 'b', move to the 'b' gate state

LOOKAHEAD_DISPATCH_ON_ENDMARKER = "lookahead $: go to q$"  # if next input is '$', move to the end-marker gate state

EXPAND_S_TO_aSb_WHEN_LOOKAHEAD_A = "expand S→aSb (la=a)"  # when gate is qa, replace S on stack with 'a S b'
EXPAND_S_TO_EPSILON_WHEN_LOOKAHEAD_B = "expand S→ε (la=b)"  # when gate is qb, remove S (use the ε production)
EXPAND_S_TO_EPSILON_AT_ENDMARKER = "expand S→ε (la=$)"  # when gate is q$, remove S at end of input
