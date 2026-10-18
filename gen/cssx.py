"""Minimal CSS rule picker for the build: keeps the rules (with their @media
wrappers) whose selector matches a pattern. Used to share the header/footer
rules of supplement-zz-refine.css with the homepage bundle."""
import re


def parse(text):
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    out, i, n = [], 0, len(text)
    while i < n:
        j = text.find("{", i)
        if j < 0:
            break
        prelude = text[i:j].strip()
        depth, k = 1, j + 1
        while k < n and depth:
            depth += {"{": 1, "}": -1}.get(text[k], 0)
            k += 1
        body = text[j + 1:k - 1]
        if prelude.startswith(("@media", "@supports")):
            out.append(("@", prelude, parse(body)))
        else:
            out.append(("r", prelude, body.strip()))
        i = k
    return out


def pick(rules, pattern):
    res = []
    for kind, prelude, body in rules:
        if kind == "@":
            inner = pick(body, pattern)
            if inner:
                res.append(("@", prelude, inner))
        elif re.search(pattern, prelude):
            res.append((kind, prelude, body))
    return res


def dump(rules, ind=""):
    out = []
    for kind, prelude, body in rules:
        if kind == "@":
            out.append(f"{ind}{prelude} {{\n{dump(body, ind + '  ')}{ind}}}\n")
        else:
            out.append(f"{ind}{prelude} {{ {body} }}\n")
    return "".join(out)
