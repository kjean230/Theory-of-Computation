# DPDA_FILE.py — constants, labels, and ordered transition table
# Problem to solve: L = { a^n b^n | n ≥ 0 }
# one-ymbol lookahead, accept by final state after consuming '$'

# Symbols and special markers
# all used in the deterministic transitions table 
EPS = "ε"        # epsilon
END = "$"        # end-marker
BOT = "⊥"        # bottom-of-stack (rightmost character = top of stack)

# States in the DPDA 
P    = "p"         # pre-init
Q    = "q"         # driver (matches terminals, dispatches lookahead)
QA   = "qa"        # lookahead gate when next input is 'a'
QB   = "qb"        # lookahead gate when next input is 'b'
QD   = "q$"        # end-marker handling
QACC = "q_accept"  # accepting (final)

STATES       = {P, Q, QA, QB, QD, QACC}
FINAL_STATES = {QACC}

# Alphabets that are only allowed in the DPDA model 
SIGMA = {"a", "b", END}       # input alphabet
GAMMA = {"S", "a", "b", BOT}  # stack alphabet

# Grammar labels (G column) for trace printing
# these will be used in the G column of the trace
G1 = "S→aSb"
G2 = "S→ε"

# Descriptive delta labels
# this will be used in the Δ column of the trace
# Note: some labels are reused for similar transitions
# all exist within the transitions table
INIT_PUSH_BOTTOM_AND_START        = "init: push ⊥ and S"
LOOKAHEAD_DISPATCH_ON_A           = "lookahead a: go to qa"
LOOKAHEAD_DISPATCH_ON_B           = "lookahead b: go to qb"
LOOKAHEAD_DISPATCH_ON_ENDMARKER   = "lookahead $: go to q$"
EXPAND_S_TO_aSb_WHEN_LOOKAHEAD_A  = "expand S→aSb (la=a)"
EXPAND_S_TO_EPSILON_WHEN_LOOKAHEAD_B = "expand S→ε (la=b)"
EXPAND_S_TO_EPSILON_AT_ENDMARKER  = "expand S→ε (la=$)"
MATCH_TERMINAL_A                  = "match terminal 'a'"
MATCH_TERMINAL_B                  = "match terminal 'b'"
FINAL_POP_BOTTOM_AND_ACCEPT       = "final: pop ⊥ and accept"

#  Table header (for printing and visual effects)
TABLE_HEADER = "step | state | unread | top | Δ | G"

# Ordered deterministic transitions: (state, input, top, next, push, label, G, consumes) 
TRANSITIONS = [

    # 0) init: push ⊥ and S
    (P,  EPS,  EPS,  Q,   f"{BOT}S",  INIT_PUSH_BOTTOM_AND_START,            "-",  False),

    # 1) lookahead dispatch while top is S (preserve S)
    (Q,  "a",  "S",  QA,  "S",        LOOKAHEAD_DISPATCH_ON_A,               "-",  False),
    (Q,  "b",  "S",  QB,  "S",        LOOKAHEAD_DISPATCH_ON_B,               "-",  False),
    (Q,  "$",  "S",  QD,  "S",        LOOKAHEAD_DISPATCH_ON_ENDMARKER,       "-",  True),   # consumes '$'

    # 2) expand S based on gate, then return to q
    (QA, EPS,  "S",  Q,   "bSa",      EXPAND_S_TO_aSb_WHEN_LOOKAHEAD_A,      G1,   False),  # push b,S,a so 'a' is on top
    (QB, EPS,  "S",  Q,   "",         EXPAND_S_TO_EPSILON_WHEN_LOOKAHEAD_B,  G2,   False),  # pop S (ε)

    # 3) match terminals (consume input)
    (Q,  "a",  "a",  Q,   "",         MATCH_TERMINAL_A,                      "-",  True),
    (Q,  "b",  "b",  Q,   "",         MATCH_TERMINAL_B,                      "-",  True),

    # 4) end handling when only ⊥ remains (consume '$', keep ⊥)
    (Q,  "$",  BOT,  QD,  BOT,        LOOKAHEAD_DISPATCH_ON_ENDMARKER,       "-",  True),

    # 5) in q$: collapse any leftover S by ε, then pop ⊥ to accept
    (QD, EPS,  "S",  QD,  "",         EXPAND_S_TO_EPSILON_AT_ENDMARKER,      G2,   False),
    (QD, EPS,  BOT,  QACC,"",         FINAL_POP_BOTTOM_AND_ACCEPT,           "-",  False),
]