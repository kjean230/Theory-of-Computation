# tests.py — quick checks for your DPDA CLI/module
from DPDA_class import DPDA  # adjust import path if needed

def run_case(s, expect_accept, expect_rows=None):
    m = DPDA()
    ok, rows = m.run(s)
    print(f"{s!r}: {'ACCEPT' if ok else 'REJECT'} ({len(rows)} rows)")
    if ok != expect_accept:
        print("  FAIL: wrong decision")
    if expect_rows is not None and len(rows) != expect_rows:
        print(f"  FAIL: expected {expect_rows} rows, got {len(rows)}")
    return ok, len(rows)

def main():
    # Accept
    run_case("$", True, 4)
    run_case("ab$", True, 9)
    run_case("aabb$", True, 13)
    run_case("aaabbb$", True, 17)
    run_case("aaaabbbb$", True, 21)
    run_case("aaaaabbbbb$", True, 25)
    run_case("aaaaaabbbbbb$", True, 29)

    # Reject
    run_case("b$", False)
    run_case("a$", False)
    run_case("abb$", False)
    run_case("aba$", False)

    # Format errors (should raise)
    for bad in ["a c$", "AABB$", "ab$$"]:
        try:
            DPDA().run(bad)
            print(f"{bad!r}: FAIL (expected error)")
        except ValueError as e:
            print(f"{bad!r}: OK error -> {e}")

if __name__ == "__main__":
    main()