"""Photos where someone is half out of frame in the original (Naman, Oct 22:
no face cut off anywhere). No crop position can fix those, so a thin strip is
trimmed off that edge of the file itself. Each entry: original size and the
share kept (left, top, right, bottom). Running again is a no-op once the file
is already at its trimmed size. Then rerun gen/qa/faces.sh.
    python3 gen/qa/trims.py"""
import json
import os
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
TRIMS = {
    "assets/img/mb/mb-209.webp": ((952, 927), (0, 0, 0.954, 1)),      # Mission Africa, child at the right edge
    "assets/img/mb/mb-355.webp": ((1600, 1200), (0, 0, 0.964, 1)),    # Meals of Love and Care, right edge
    "assets/img/mb/mb-703.webp": ((1600, 900), (0, 0, 0.970, 1)),     # NYC gala room, guest at the right edge
    "assets/img/mb/mb-360.webp": ((1600, 1200), (0, 0, 0.880, 1)),    # Indiana, girl at the right edge
    "assets/img/mb/mb-716.webp": ((1600, 1066), (0.031, 0, 0.973, 1)),  # gala audience, both edges
}


def main():
    faces = {}
    for line in open(os.path.join(ROOT, "gen", "qa", "faces.jsonl")):
        d = json.loads(line)
        faces[d["file"]] = d["faces"]
    for path, ((w0, h0), (l, t, r, b)) in TRIMS.items():
        full = os.path.join(ROOT, path)
        im = Image.open(full)
        if im.size != (w0, h0):
            print(f"{path}: already trimmed {im.size}")
            continue
        # every other face must stay whole with the new edges
        for x, y, fw, fh, _ in faces.get(path, []):
            cut = (x < l < x + fw) or (x < r < x + fw) or (y < t < y + fh) or (y < b < y + fh)
            assert not cut, f"{path}: trim would cut the face at {x:.3f},{y:.3f}"
        box = (round(l * w0), round(t * h0), round(r * w0), round(b * h0))
        im.crop(box).save(full, "WEBP", quality=86, method=6)
        print(f"{path}: {im.size} -> {Image.open(full).size}")


if __name__ == "__main__":
    main()
