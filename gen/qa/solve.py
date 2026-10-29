"""Re-solve every photo that still has a main-subject problem in an audit
(audit.mjs output files given as arguments) and write the result into
gen/data_faces.py. Heroes: measured windows above 860px, the fixed square box
481-860px, the fixed 39:64 box on phones. Everything else: measured windows
per width band.
    python3 gen/qa/solve.py audit-*.json"""
import json, os, sys, re, ast
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fit import heads, FACES

QA = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(QA, '..', 'data_faces.py')
seen, issues = [], []
for f in sys.argv[1:]:
    d = json.load(open(f)); seen += d['seen']; issues += d['issues']
SUBJECT = 0.035
DIMS = {'/' + json.loads(l)['file']: (json.loads(l)['w'], json.loads(l)['h']) for l in open(os.path.join(QA, 'faces.jsonl'))}

def is_major(i):
    x, y, w, h, c = FACES[i['src']][i['face']]
    return h >= SUBJECT and not (x < -0.002 or y < -0.002 or x + w > 1.002 or y + h > 1.002)
fp = 'flipcard__front|photocard__frame'
todo = sorted(set(i['src'] for i in issues if is_major(i) and not i['status'].startswith('HAIR') and not re.search(fp, i['where'])))

def score(hs, wins, px, py):
    cut = text = hair = bg = inn = 0
    for wx, wy, hero in wins:
        l, t = px * (1 - wx), py * (1 - wy); r, b = l + wx, t + wy
        for hl, ht, hr, hb, (fl, ft, fr, fb) in hs:
            major = fb - ft >= SUBJECT
            if hr <= l or hl >= r or hb <= t or ht >= b: continue
            cl, ct, cr, cb = max(fl, 0), max(ft, 0), min(fr, 1), min(fb, 1)
            if not (cl >= l - 1e-4 and cr <= r + 1e-4 and ct >= t - 1e-4 and cb <= b + 1e-4):
                if major: cut += 1
                else: bg += 1
                continue
            if (cl, ct, cr, cb) != (fl, ft, fr, fb): bg += 1; continue
            if major:
                inn += 1
                if not (hl >= l - 1e-4 and hr <= r + 1e-4 and ht >= t - 1e-4 and hb <= b + 1e-4): hair += 1
                if hero and (fb - t) / wy > 0.68 and (fl - l) / wx < 0.65: text += 1
    return cut, text, hair, bg, inn

def best(hs, wins, cur):
    res = []
    for px in range(0, 101, 2):
        for py in range(0, 101, 2):
            c, tx, h, g, i = score(hs, wins, px / 100, py / 100)
            res.append((c, tx, h, g, -i, abs(px - cur[0]) + abs(py - cur[1]), px, py))
    return min(res)

def box(A, B):  # window for a box of aspect B over a photo of aspect A (cover)
    R = B / A
    return (min(1, R), min(1, 1 / R))

new = {}
for src in todo:
    hs = heads(src); pl = [s for s in seen if s['src'] == src]
    hero = any('pagehead' in s['where'] for s in pl)
    A = DIMS[src][0] / DIMS[src][1]
    groups = {'pos': [], 'md': [], 'sm': []}; cur = None
    for s in pl:
        wx, wy = s['V']['r'] - s['V']['l'], s['V']['b'] - s['V']['t']
        if cur is None:
            cur = (round(100 * s['V']['l'] / (1 - wx)) if wx < .999 else 50, round(100 * s['V']['t'] / (1 - wy)) if wy < .999 else 50)
        h = 'pagehead' in s['where']
        if h and s['w'] <= 860: continue
        groups['pos' if s['w'] > 860 else 'md' if s['w'] > 480 else 'sm'].append((wx, wy, h))
    if hero:
        groups['md'].append(box(A, 1) + (True,)); groups['sm'].append(box(A, 39 / 64) + (True,))
    allw = [w for g in groups.values() for w in g]
    one = best(hs, allw, cur)
    if one[0] == 0 and one[1] == 0:
        new[src] = f'{one[6]}% {one[7]}%'; q = one[:5]
    else:
        g = {k: best(hs, w, cur) for k, w in groups.items() if w}
        new[src] = {k: f'{v[6]}% {v[7]}%' for k, v in g.items()}; q = {k: v[:5] for k, v in g.items()}
    print(src.split('/')[-1].ljust(16), new[src], q)

s = open(SITE).read()
head, body = s.split('FACE_POS = {', 1)
end = body.index('\n}\n') + 3  # FACE_POS ends at the first closing brace on its own line
body, tail = body[:end], body[end:]
cur_map = ast.literal_eval('{' + body)
cur_map.update(new)
lines = ['FACE_POS = {']
for k in sorted(cur_map):
    v = cur_map[k]
    val = f'"{v}"' if isinstance(v, str) else '{' + ', '.join(f'"{a}": "{b}"' for a, b in v.items()) + '}'
    lines.append(f'    "{k}": {val},')
open(SITE, 'w').write(head + '\n'.join(lines) + '\n}\n' + tail)
print(len(new), 'updated,', len(cur_map), 'total')
