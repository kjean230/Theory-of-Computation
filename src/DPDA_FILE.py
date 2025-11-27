# DPDA_FILE.py (deterministic pushdown automata file operations)
# dpda.py — DPDA for L = { a^n b^n } with one-symbol lookahead

# Special Symbols
EPS = 'ε' # this represents the empty string (EPSILON) - no input
BOT = '⊥' # this represents the bottom stack symbol
END = '$' # the input endmarker symbol

P = 'p' # the pre-initial state (before pushing any inputs)
Q = 'q' # the driver state (dispatches lookahead)
QA = 'qa' # the gate state (if next input symbol is 'a')
QB = 'qb' # the gate state (if next input symbol is 'b')
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

HANDOFF_BACK_TO_DRIVER_AFTER_PUSHING_A = "handoff: qa on 'a' → q"  # after pushing an 'a', return control from qa to q
HANDOFF_BACK_TO_DRIVER_AFTER_PUSHING_B = "handoff: qb on 'b' → q"  # after pushing a 'b', return control from qb to q

MATCH_TERMINAL_A = "match terminal 'a'"  # when top is 'a' and next input is 'a', pop it and advance
MATCH_TERMINAL_B = "match terminal 'b'"  # when top is 'b' and next input is 'b', pop it and advance
FINAL_POP_BOTTOM_AND_ACCEPT = "final: pop ⊥ and accept"  # when only ⊥ remains, pop it and move to the accepting state

# ----- Ordered transition list: (state, input, top, next, push, label, G, consumes) -----
TABLE_HEADER = "step | state | unread | top | Δ | G"  # header line for the output table

# ---- transitions representation, matching the table header ---- #
TRANSITIONS = [  # (state, input, top, next, push, label, G, consumes)

    # 0) init: push ⊥ and S
    (P,  EPS,  EPS,  Q,   f"{BOT}S",  INIT_PUSH_BOTTOM_AND_START,              "-",    False),

    # 1) lookahead dispatch while top is S (do NOT change stack; preserve S)
    (Q,  "a",  "S",  QA,  "S",        LOOKAHEAD_DISPATCH_ON_A,                 "-",    False),
    (Q,  "b",  "S",  QB,  "S",        LOOKAHEAD_DISPATCH_ON_B,                 "-",    False),
    (Q,  "$",  "S",  QD,  "S",        LOOKAHEAD_DISPATCH_ON_ENDMARKER,         "-",    True),   # consume '$'

    # 2) expand S based on the gate, then return to q
    (QA, EPS,  "S",  Q,   "bSa",      EXPAND_S_TO_aSb_WHEN_LOOKAHEAD_A,        G1,     False),  # push b,S,a so 'a' is on top
    (QB, EPS,  "S",  Q,   "",         EXPAND_S_TO_EPSILON_WHEN_LOOKAHEAD_B,    G2,     False),  # pop S (ε)

    # 3) match terminals (consume input)
    (Q,  "a",  "a",  Q,   "",         MATCH_TERMINAL_A,                        "-",    True),
    (Q,  "b",  "b",  Q,   "",         MATCH_TERMINAL_B,                        "-",    True),

    # 4) end handling when only ⊥ remains (consume '$', keep ⊥ so q$ can pop it)
    (Q,  "$",  BOT,  QD,  BOT,        LOOKAHEAD_DISPATCH_ON_ENDMARKER,         "-",    True),

    # 5) in q$: collapse any leftover S by ε, then pop ⊥ to accept
    (QD, EPS,  "S",  QD,  "",         EXPAND_S_TO_EPSILON_AT_ENDMARKER,        G2,     False),
    (QD, EPS,  BOT,  QACC,"",         FINAL_POP_BOTTOM_AND_ACCEPT,             "-",    False),
]
