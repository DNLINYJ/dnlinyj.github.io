#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solver for 20250805Calc-based C# crackme.
Implements:
- SN decoder (digit run-length with 'l' and optional '.')
- Name -> A
- Decimal division with arbitrary precision
- Quotient extraction like the C# program
- Blocked linear-relation verifier
- Heuristic search over short SN patterns (editable)
"""

from decimal import Decimal, getcontext
import sys
from typing import Optional, Tuple

# ------------------------------
# Core: SN decoder (faithful to C#)
# ------------------------------
def decode_sn(sn: str) -> Optional[str]:
    """
    Decode the custom SN encoding into a string B consisting of digits and optionally a single '.'
    Returns None if invalid by the C# rules.
    """
    if len(sn) < 26 or len(sn) > 50:
        return None
    if sn.startswith('0'):
        return None
    if sn.endswith('.'):
        return None

    out = []
    c = None            # current digit char
    cnt_s = ""          # accumulating count text
    dot_allowed_here = True
    last_num = 0

    for ch in sn:
        if '0' <= ch <= '9':
            if c is None:
                c = ch
                cnt_s = ""
            else:
                # leading zero in count is invalid
                if cnt_s == "" and ch == '0':
                    return None
                cnt_s += ch
            dot_allowed_here = False
        elif ch == 'l':
            if dot_allowed_here:
                return None
            if c is None:
                return None
            if cnt_s == "":
                return None
            if last_num != 0:
                return None
            try:
                last_num = int(cnt_s)
            except:
                return None
            if last_num == 0:
                return None
            out.append(c * last_num)
            last_num = 0
            c = None
            cnt_s = ""
            dot_allowed_here = True
        elif ch == '.':
            # place '.' literally between runs, with strict guards
            if not out:
                return None
            if cnt_s != "":
                return None
            if c is not None and cnt_s == "":
                return None
            out.append('.')
            c = None
            cnt_s = ""
            dot_allowed_here = True
        else:
            return None

    # Handle trailing run if any
    if not dot_allowed_here:
        if not out:
            return None
        if c is None:
            return None
        if cnt_s == "":
            return None
        if last_num != 0:
            return None
        try:
            last_num = int(cnt_s)
        except:
            return None
        if last_num == 0:
            return None
        out.append(c * last_num)

    return "".join(out)


# ------------------------------
# Name -> A (per C#)
# ------------------------------
def name_to_A(name: str) -> str:
    b = 0
    for byte in name.encode('utf-8'):
        b ^= byte
    num = b % 64
    if num % 2 == 0:
        num += 1
    return str(num)


# ------------------------------
# External decimal division (per 20250805Calc-pub.py)
# ------------------------------
def calc_decimal_division(A: str, B: str, precision: int) -> str:
    # mirror the Python helper
    getcontext().prec = int(precision)
    x = Decimal(A) / Decimal(B)
    # Python's Decimal.__str__ is what the C# program reads off stdout
    return str(x)


# ------------------------------
# C# Quotient extractor
# ------------------------------
def make_quotient_from_text(text: str) -> Optional[str]:
    """
    Implements KX_TXlEaXZpZGU雪's logic:
    - If text contains 'E':
        - split by '.', 'E', '-' (in any order)
        - Quotient = '1' + array[1]   (digits after the '.')
        - If text contains '-': left-pad with (exponent - 1) zeros
    Else:
        return None (C# leaves it empty and later fails)
    """
    if not text or 'E' not in text:
        return None

    # emulate String.Split(new char[] {'.','E','-'})
    parts = []
    cur = ""
    for ch in text:
        if ch in ".E-":
            if cur != "":
                parts.append(cur)
                cur = ""
            else:
                # consecutive separators produce empty string entries in C#
                parts.append("")
        else:
            cur += ch
    if cur != "":
        parts.append(cur)

    # After splitting, array[1] should be the digits after '.' (or empty)
    if len(parts) < 2:
        return None
    frac = parts[1]  # may be empty when original had no '.' like '1E-7'
    q = "1" + frac

    if '-' in text:
        try:
            exp = int(parts[-1])
        except:
            return None
        target_len = len(q) + exp - 1
        if target_len > len(q):
            q = q.rjust(target_len, '0')
    return q


# ------------------------------
# String arithmetic like C#
# ------------------------------
def str_add(a: str, b: str) -> str:
    if len(a) < len(b):
        a, b = b, a
    carry = 0
    out = []
    ia = len(a) - 1
    ib = len(b) - 1
    while ia >= 0 or ib >= 0 or carry:
        da = ord(a[ia]) - 48 if ia >= 0 else 0
        db = ord(b[ib]) - 48 if ib >= 0 else 0
        s = da + db + carry
        out.append(chr(48 + (s % 10)))
        carry = s // 10
        ia -= 1
        ib -= 1
    return "".join(reversed(out))


def str_mul_small(s: str, k: int) -> str:
    carry = 0
    out = []
    for ch in reversed(s):
        d = ord(ch) - 48
        val = d * k + carry
        out.append(chr(48 + (val % 10)))
        carry = val // 10
    while carry:
        out.append(chr(48 + (carry % 10)))
        carry //= 10
    # 与 C# 的 KX_TXVsdGlTdHJpbmdz 一致：不去前导 0，保持块宽度
    res = "".join(reversed(out))
    # 正常情况下 res 长度 >= len(s)，若无最高位进位则恰为 len(s)
    if len(res) < len(s):
        res = res.rjust(len(s), '0')
    return res


# ------------------------------
# Verification (per KX_VmVyaWZ5U2lnbmFs & main loop)
# ------------------------------
def verify_quotient(quotient: str, num2: int = 2040, num3: int = 2025) -> Tuple[bool, int]:
    """
    Returns (ok, j_end) where ok means the program would print Congratulations!
    and j_end is the j value after the break (=num2-3 when ok).
    """
    # early length sanity
    # we will read up to block (j+3), j can be as large as 2036 before break, so we need (2039+1)*num3 at least
    # but just rely on try/except like C#
    j = 0
    try:
        while j < num2:
            s0 = quotient[j * num3:(j + 1) * num3]
            s1 = quotient[(j + 1) * num3:(j + 2) * num3]
            s2 = quotient[(j + 2) * num3:(j + 3) * num3]
            s3 = quotient[(j + 3) * num3:(j + 4) * num3]
            if s0 == s1 == s2:
                j = 2**31 - 1  # int.MaxValue
            lhs = str_add(str_add(str_mul_small(s0, 5), str_mul_small(s1, 8)), str_mul_small(s2, 9))
            if s3 != lhs:
                j += 1
                break
            j += 1
        ok = (j == num2 - 3)
        return ok, j
    except Exception:
        return False, j


# ------------------------------
# Helpers to build pipeline
# ------------------------------
def pipeline_from_sn(name: str, sn: str, precision: int = (2040+1)*2025) -> Tuple[bool, Optional[str], Optional[str], Optional[int]]:
    A = name_to_A(name)
    B = decode_sn(sn)
    if B is None or not A or A.endswith('0') or B.endswith('0'):
        return False, A, None, None

    text = calc_decimal_division(A, B, precision)
    q = make_quotient_from_text(text)
    if not q:
        return False, A, B, None

    ok, j = verify_quotient(q, 2040, 2025)
    return ok, A, B, j


# ------------------------------
# Very small heuristic search (edit to expand)
# Generates SNs of the shape: d1 cnt1 l [.] d2 cnt2 l [d3 cnt3 l]
# where counts are chosen to keep total length in [26,50].
# ------------------------------

def search_sn_for_name(name: str, max_checks: int = 500):
    """
    Generate candidate SNs with 5-6 runs so that the SN textual length is within [26, 50].
    Counts are ~4k-8k to keep decoded B length ~30k-50k digits.
    We insert at most one '.' between runs (never first/last), and ensure SN doesn't end with '.'.
    """
    candidates = []
    digits_pool = ['9','7','3','1','2','5','8']  # avoid '0' for tail constraint
    count_pool  = [4096, 5000, 6074, 7000, 8191] # ~4k-8k, mixed
    run_counts  = [5, 6]  # number of runs

    def build_runs(runs, dot_pos=None):
        parts = []
        for i, (d, c) in enumerate(runs):
            parts.append(f"{d}{c}l")
            if dot_pos is not None and i == dot_pos:
                parts.append(".")
        sn = "".join(parts)
        return sn

    # Produce permutations of runs (limited breadth)
    for R in run_counts:
        # Simple cyclic pattern of digits to avoid triple-equal blocks in the earliest area
        for d0 in digits_pool[:4]:
            for d1 in digits_pool[1:5]:
                for d2 in digits_pool[2:6]:
                    # choose counts pattern
                    for c0 in count_pool:
                        for c1 in count_pool:
                            for c2 in count_pool:
                                base_runs = [(d0,c0),(d1,c1),(d2,c2)]
                                # fill remaining with mirrored counts/digits
                                extra = []
                                pool = list(zip(reversed(digits_pool[:4]), reversed(count_pool)))
                                while len(base_runs) + len(extra) < R:
                                    extra.append(pool[(len(extra)) % len(pool)])
                                runs = base_runs + extra
                                # dot positions: after 2nd or 3rd run (index 1 or 2), or no dot
                                for dot_pos in [None, 1, 2]:
                                    sn = build_runs(runs, dot_pos=dot_pos)
                                    if 26 <= len(sn) <= 50 and not sn.endswith('.'):
                                        candidates.append(sn)
                                    if len(candidates) >= max_checks:
                                        break
                                if len(candidates) >= max_checks:
                                    break
                            if len(candidates) >= max_checks:
                                break
                        if len(candidates) >= max_checks:
                            break
                    if len(candidates) >= max_checks:
                        break
                if len(candidates) >= max_checks:
                    break
            if len(candidates) >= max_checks:
                break
        if len(candidates) >= max_checks:
            break

    # Deduplicate while preserving order
    seen = set()
    ordered = []
    for s in candidates:
        if s not in seen:
            seen.add(s)
            ordered.append(s)

    print(f"[search] Generated {len(ordered)} candidate SNs (trying {min(len(ordered), max_checks)}).")
    for idx, sn in enumerate(ordered[:max_checks], 1):
        ok, A, B, j = pipeline_from_sn(name, sn)
        if ok:
            print(f"[FOUND] SN = {sn}")
            print(f"  A={A}")
            print(f"  B (decoded) begins: {B[:60]}{'...' if len(B)>60 else ''}")
            print(f"  Break j = {j} (expect 2037 to pass)")
            return sn
        if idx % 10 == 0:
            print(f"  tried {idx} / {len(ordered)}")
    print("[search] No solution found in this small search set. Try increasing --search and broadening pools.")
    return None



# ------------------------------
# Deterministic constructor (polynomial-denominator method)
# D = 10^(3m) - 9*10^(2m) - 8*10^(m) - 5  with m=2025
# Choose B = A * D so that A/B = 1/D which normalizes near "1.xxxxxE-..."
# ------------------------------
def _build_D_digits(m: int = 2025) -> str:
    L = 3*m + 1
    digs = ['0'] * L
    digs[0] = '1'
    def sub_at_power(power: int, amount: int):
        idx = L - 1 - power
        carry = amount
        i = idx
        while carry > 0 and i >= 0:
            cur = ord(digs[i]) - 48
            if cur >= (carry % 10):
                new = cur - (carry % 10)
                digs[i] = chr(48 + new)
                carry //= 10
            else:
                new = cur + 10 - (carry % 10)
                digs[i] = chr(48 + new)
                carry = carry // 10 + 1
            i -= 1
    sub_at_power(2*m, 9)
    sub_at_power(1*m, 8)
    sub_at_power(0, 5)
    return "".join(digs)

def _mul_small_str(num_str: str, k: int) -> str:
    carry = 0
    out = []
    for ch in reversed(num_str):
        d = ord(ch) - 48
        val = d * k + carry
        out.append(chr(48 + (val % 10)))
        carry = val // 10
    while carry:
        out.append(chr(48 + (carry % 10)))
        carry //= 10
    return "".join(reversed(out))

def _rle_digits(s: str):
    runs=[]
    if not s:return runs
    cur=s[0];cnt=1
    for ch in s[1:]:
        if ch==cur:cnt+=1
        else:
            runs.append((cur,cnt))
            cur=ch;cnt=1
    runs.append((cur,cnt))
    return runs

def _encode_runs_to_sn(runs, omit_last_l=True, insert_dot_after_index: int = None) -> str:
    parts=[]
    for i,(d,cnt) in enumerate(runs):
        parts.append(f"{d}{cnt}l")
        if insert_dot_after_index is not None and i == insert_dot_after_index:
            parts.append(".")
    s="".join(parts)
    if omit_last_l and s.endswith('l'):
        s=s[:-1]
    # guard: constraints
    if s.endswith('.') or s.startswith('0') or len(s)<26 or len(s)>50:
        return ""
    return s

def deterministic_sn_for_name(name: str, m: int = 2025) -> str:
    A = int(name_to_A(name))
    D = _build_D_digits(m)
    B = _mul_small_str(D, A)         # B = A * D
    runs = _rle_digits(B)
    # Try to encode with trailing 'l' omitted
    sn = _encode_runs_to_sn(runs, omit_last_l=True, insert_dot_after_index=None)
    if 26 <= len(sn) <= 50:
        return sn
    # If too long, try placing one '.' early (doesn't help length, but try)
    for idx in [1,2,3]:
        sn = _encode_runs_to_sn(runs, omit_last_l=True, insert_dot_after_index=idx)
        if 26 <= len(sn) <= 50:
            return sn
    return ""

def run_deterministic(name: str):
    sn = deterministic_sn_for_name(name, 2025)
    if not sn:
        print("[deterministic] Could not pack SN to 26-50 chars; consider tweaking encoding.")
        return
    print(f"[deterministic] SN (encoded): {sn} (len={len(sn)})")
    ok, A, B, j = pipeline_from_sn(name, sn)
    print(f"A={A}")
    if B is None:
        print("Decode failed unexpectedly.")
        return
    print(f"Decoded B head: {B[:60]}...")
    print(f"Verify: {'PASS' if ok else 'FAIL'}; j={j} (expect {2040-3})")
    if ok:
        print("Congratulations! Deterministic construction succeeded.")
    else:
        print("Deterministic SN constructed but did not pass; adjust m or verify logic.")

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="KCTF")
    ap.add_argument("--sn", help="Test a specific SN (encoded).", default=None)
    ap.add_argument("--search", action="store_true", help="Run a small heuristic search over SN patterns.")
    ap.add_argument("--deterministic", action="store_true", help="Use deterministic constructor to output an SN for the given name.")
    args = ap.parse_args()

    if args.deterministic:
        run_deterministic(args.name)
        return

    if args.sn:
        ok, A, B, j = pipeline_from_sn(args.name, args.sn)
        print(f"Name={args.name}, A={A}")
        print(f"SN={args.sn}")
        if B is None:
            print("Decode failed / invalid SN encoding.")
            sys.exit(2)
        print(f"Decoded B (head 120): {B[:120]}{'...' if len(B)>120 else ''}")
        if B.endswith('0') or A.endswith('0'):
            print("A or B ends with 0 -> immediate rejection by program.")
        text = calc_decimal_division(A, B, (2040+1)*2025)
        q = make_quotient_from_text(text)
        if q is None:
            print("Python output had no 'E' or parsing failed; program would fail.")
            sys.exit(3)
        print(f"Quotient length = {len(q)} digits")
        ok, j = verify_quotient(q, 2040, 2025)
        print(f"Verify: {'PASS (Congratulations!)' if ok else 'FAIL'}; j after break = {j}")
        sys.exit(0 if ok else 1)

    if args.search:
        res = search_sn_for_name(args.name)
        if res:
            print(f"Candidate SN that passes: {res}")
        else:
            print("No candidate found in this search configuration.")
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
