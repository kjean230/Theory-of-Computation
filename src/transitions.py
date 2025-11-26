# Static definitions for a DPDA recognizing L = { a^n b^n } with one-symbol lookahead.

EPS = "ε"      # epsilon (no input consumed)
END = "$"      # end-marker
BOT = "⊥"      # bottom-of-stack

# Input and stack alphabets
SIGMA = {"a", "b", END}
GAMMA = {"S", "a", "b", BOT}

# States
P = "p"          # pre-init
Q = "q"          # driver
QACC = "q_accept"

STATES = {P, Q, QACC}
FINAL_STATES = {QACC}

# Pretty labels for table (Δ = transition, G = grammar)
G1 = "S→aSb"
G2 = "S→ε"

GRAMMAR_TEXT = {"G1": G1, "G2": G2}
DELTA_TEXT = {
    "D1":  "(p,ε,ε) → (q,⊥S)",
    "D2":  "(q,ε,S) → (q,aSb)   [la=a]",
    "D3":  "(q,ε,S) → (q,ε)     [la=b/$]",
    "D4":  "(q,a,a) → (q,ε)",
    "D5":  "(q,b,b) → (q,ε)",
    "D6":  "(q,$,⊥) → (q_accept,ε)",
}

# Transition list:
# (state, input_symbol, stack_top, next_state, push_string, delta_label, grammar_label, consumes_input)
# Rightmost char of push_string is stack top; "" means push ε (i.e., pop only).
TRANSITIONS = [
    # Initialize stack with ⊥S
    (P,  EPS,  EPS,  Q,    f"{BOT}S", "D1",  "-",  False),

    # Grammar expansions (top-down) decided by one-symbol lookahead, but without consuming input
    # S → aSb when next input is 'a'
    (Q,  EPS,  "S",  Q,    "aSb",     "D2",  "G1", False),
    # S → ε when next input is 'b' or '$'
    (Q,  EPS,  "S",  Q,    "",        "D3",  "G2", False),

    # Terminal matches
    (Q,  "a",  "a",  Q,    "",        "D4",  "-",  True),
    (Q,  "b",  "b",  Q,    "",        "D5",  "-",  True),

    # End handling: consume $ when stack reduced to ⊥ and accept
    (Q,  END,  BOT,  QACC, "",        "D6",  "-",  True),
]
# Note: In the push_string, the leftmost character will be at the top of the stack after the push.
# For example, pushing "aSb" means 'b' is at the top, then 'S', then 'a' at the bottom of that push.
# This is because stacks are typically visualized with the top on the right side.
# The transitions are designed to ensure that the DPDA can only accept strings of the form a^n b^n.
# The one-symbol lookahead allows the DPDA to decide which grammar rule to apply without ambiguity. 
# The DPDA will reject any input that does not conform to the language L = { a^n b^n }.