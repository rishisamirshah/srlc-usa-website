#!/usr/bin/env python3
"""Localize curated Media Bank photos and regenerate gen/data_media.py.

usage: python gen/media_fetch.py <curation.json> <sheet_index.json> [--min-q 3]

curation.json: {"photos": [{n, id, keep, q, orient, tags, hero, alt}], "slots": {slot: [n, ...]}}
sheet_index.json: [{n, id, path, folder}] from the Media Bank contact sheets.
The Drive folder is link-shared, so thumbnails download without auth."""
import io, json, os, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "mb")
SKIP_TAGS = {"spiritual", "sarvamangal"}
# Hand picks that win over the curator's first choice. home-impact-story: no
# identifiable patient beside Laxmibhai's story, subject in the left half for
# the fixed-background parallax panel.
SLOT_OVERRIDES = {
    "home-impact-story": 123,
    "card-volunteer": 9,      # school-kit packing; the PB&J line is already hero slide 2
    "management-hero": 727,   # guests at the gala, not one identifiable speaker under stage light
}
# Minimum source width per slot family: full-bleed heroes, half-width splits,
# square cards. A slot with no candidate this wide is left out so the page's
# size-aware pool route fills it instead.
SLOT_MIN = (("hero", 1600), ("care-", 1600), ("wwa-", 1200), ("home-impact-story", 1000), ("card-", 700), ("inst-", 700))


def slot_min(name):
    return next((w for k, w in SLOT_MIN if k in name), 0)


def fetch(item):
    n, fid, width = item
    dst = os.path.join(OUT, f"mb-{n}.webp")
    if os.path.exists(dst) and os.path.getsize(dst) > 5000:
        with Image.open(dst) as im:
            return n, im.size
    url = f"https://drive.google.com/thumbnail?id={fid}&sz=w{width}"
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60) as r:
                data = r.read()
            im = Image.open(io.BytesIO(data)).convert("RGB")
            if im.width > width:
                im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
            im.save(dst, "WEBP", quality=74, method=6)
            return n, im.size
        except Exception as e:
            err = e
    print(f"  ! mb-{n}: {err}")
    return n, None


def main():
    cur = json.load(open(sys.argv[1], encoding="utf-8"))
    folders = {o["n"]: o["folder"] for o in json.load(open(sys.argv[2], encoding="utf-8"))}
    min_q = int(sys.argv[sys.argv.index("--min-q") + 1]) if "--min-q" in sys.argv else 3
    photos = {p["n"]: p for p in cur["photos"] if p.get("keep")}
    options = {name: ([SLOT_OVERRIDES[name]] if name in SLOT_OVERRIDES else [n for n in cands if n in photos])
               for name, cands in cur.get("slots", {}).items()}
    pool = [p for p in photos.values()
            if p.get("q", 0) >= min_q and not (set(p.get("tags", [])) & SKIP_TAGS)
            and not ("render" in p.get("tags", []) and "jivamaitridham" not in p.get("tags", []))]
    wanted = {p["n"] for p in pool} | {n for opts in options.values() for n in opts}
    hero_ns = {n for s, opts in options.items() if slot_min(s) >= 1600 for n in opts}
    os.makedirs(OUT, exist_ok=True)
    jobs = [(n, photos[n]["id"], 2000 if n in hero_ns or photos[n].get("hero") else 1600) for n in sorted(wanted)]
    with ThreadPoolExecutor(8) as ex:
        sizes = dict(ex.map(fetch, jobs))
    slots = {}
    for name, opts in options.items():
        ok = [n for n in opts if sizes.get(n) and sizes[n][0] >= slot_min(name)]
        if ok:
            slots[name] = ok[0]

    def entry(n):
        w, h = sizes[n]
        return (f"/assets/img/mb/mb-{n}.webp", w, h, photos[n].get("alt", "").replace('"', "'"))

    slot_lines = [f'    "{s}": {entry(n)!r},' for s, n in sorted(slots.items()) if sizes.get(n)]
    pool_sorted = sorted((p for p in pool if sizes.get(p["n"])),
                         key=lambda p: (-p.get("q", 0), p.get("orient") != "land", p["n"]))
    pool_lines = []
    for p in pool_sorted:
        src, w, h, alt = entry(p["n"])
        # src:<folder> marks the shoot a photo came from, so a gallery can avoid
        # showing one event from three angles
        src_tag = "src:" + folders.get(p["n"], "").strip("/").lower().replace(" ", "-")
        pool_lines.append(f"    ({src!r}, {tuple(p.get('tags', []) + [src_tag])!r}, {w}, {h}, {alt!r}),")
    out = ['"""Media Bank photography (Drive "General Media Bank"), localized into',
           'assets/img/mb/ by gen/media_fetch.py. SLOTS are named picks for specific image',
           'slots; POOL feeds every other slot by subject tag. Regenerated, not hand-edited."""',
           "", "SLOTS = {  # slot -> (src, w, h, alt)", *slot_lines, "}", "",
           "POOL = [  # (src, tags, w, h, alt), best first", *pool_lines, "]", "", "",
           "def slot(name, fallback=None):",
           '    """(src, w, h, alt) for a named slot, or the fallback tuple."""',
           "    return SLOTS.get(name, fallback)", ""]
    open(os.path.join(ROOT, "gen", "data_media.py"), "w", encoding="utf-8", newline="\n").write("\n".join(out))
    total = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT))
    print(f"{len(slot_lines)} slots, {len(pool_lines)} pool photos, {len(os.listdir(OUT))} files, {total / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
