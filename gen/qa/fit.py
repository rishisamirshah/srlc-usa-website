"""Crop solver: for a photo's detected faces and the visible fraction (wx, wy)
at each width, which object-positions keep every face fully in or fully out.
Head box = face box widened 20% each side, 45% above, 10% below."""
import json, sys

FACES = {}
for l in open(__file__.rsplit('/', 1)[0] + '/faces.jsonl'):
    d = json.loads(l); FACES['/' + d['file']] = d['faces']

def heads(src):
    out = []
    for x, y, w, h, c in FACES[src]:
        out.append((max(0, x - .2 * w), max(0, y - .45 * h), min(1, x + 1.2 * w), min(1, y + 1.1 * h), (x, y, x + w, y + h)))
    return out

def check(src, wx, wy, px, py):
    """(cut count, in count) for object-position px, py (0..1)."""
    l, t = px * (1 - wx), py * (1 - wy); r, b = l + wx, t + wy
    cut = inn = 0
    for hl, ht, hr, hb, (fl, ft, fr, fb) in heads(src):
        inside = hl >= l - 1e-4 and hr <= r + 1e-4 and ht >= t - 1e-4 and hb <= b + 1e-4
        disjoint = hr <= l or hl >= r or hb <= t or ht >= b
        if inside: inn += 1
        elif not disjoint: cut += 1
    return cut, inn

def solve(src, windows, py_options=None, px_options=None):
    """windows: list of (wx, wy). Returns best (px, py) list sorted by (cuts, -in)."""
    pxs = px_options or [i / 100 for i in range(101)]
    pys = py_options or [i / 100 for i in range(101)]
    res = []
    for px in pxs:
        for py in pys:
            cuts = ins = 0
            for wx, wy in windows:
                c, i = check(src, wx, wy, px, py); cuts += c; ins += i
            res.append((cuts, -ins, abs(px - .5) + abs(py - .5), px, py))
    res.sort()
    return res

if __name__ == '__main__':
    src = sys.argv[1]; wins = json.loads(sys.argv[2])
    for r in solve(src, wins)[:8]: print(r)
