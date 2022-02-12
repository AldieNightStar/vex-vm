from dataclasses import dataclass
from typing import Any, List, Tuple

T_SPC = "SPC"
T_NUM = "NUM"
T_STR = "STR"

@dataclass
class Token:
    type: str
    value: Any
    count: int


def lex(src: str) -> List[Token]:
    pos = 0
    toks = []
    while pos < len(src):
        if src[pos] in " \t\n\r\0":
            pos += 1
            continue
        # Parse strings
        t = lex_str(src[pos:])
        if t:
            pos += t.count
            toks.append(t)
            continue
        t = lex_num(src[pos:])
        if t:
            pos += t.count
            toks.append(t)
            continue
        # Parse comments
        commentSize = lex_comment(src[pos:])
        if commentSize != None and commentSize > 0:
            pos += commentSize
            # Do not add anything to tokens. It just a comment. It will be ignored
            continue
        t = lex_spec(src[pos:])
        if t:
            pos += t.count
            toks.append(t)
            continue
    return toks


def lex_str(s) -> Token:
    if (len(s) < 2):
        return None
    if not s[0] in "\"'`":
        return None
    sb = []
    esc = False
    end = s[0]
    for c in s[1:]:
        if (esc):
            if c == "n":
                sb.append("\n")
            elif c == "0":
                sb.append("\0")
            elif c == "t":
                sb.append("\t")
            else:
                sb.append(c)
            esc = False
            continue
        if (c == '\\'):
            esc = True
            continue
        if (c == end):
            break
        sb.append(c)
    if len(sb) < 1:
        return None
    return Token(T_STR, "".join(sb), len(sb) + 2)


def lex_num(s) -> Token:
    sb = []
    for c in s:
        if not c in "0123456789.":
            break
        sb.append(c)
    try:
        n = float("".join(sb))
        return Token(T_NUM, n, len(sb))
    except:
        return None


def lex_comment(s) -> int:
    if len(s) < 1: return None
    if s[0] != "#": return None
    cnt = 0
    for c in s:
        if c in "\n\r\0": break
        cnt += 1
    return cnt

def lex_spec(s) -> Token:
    if len(s) < 1:
        return None
    sb = []
    for c in s:
        if c in " \t\n\0\r":
            break
        sb.append(c)
    if len(sb) < 1:
        return None
    return Token(T_SPC, "".join(sb), len(sb))
