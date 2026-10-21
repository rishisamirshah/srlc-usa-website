"""Global SRLC figures, read at build time from the counters on the main SRLC
site (loveandcare.srmd.org) so these pages follow it without hand edits
(Naman, Oct 21). The last good read is cached in stats_live.json; the build
falls back to it whenever the main site can't be reached, its counters can't
be read, or a figure looks wrong. SRLC_STATS_OFFLINE=1 skips the fetch."""
import json
import os
import re
import sys
import urllib.request

SOURCE = "https://loveandcare.srmd.org/"
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stats_live.json")

# key -> (bold label on the main site, a word from its caption that tells two
# "LIVES" counters apart)
COUNTERS = {
    "lives": ("LIVES", "touched"),
    "patients": ("PATIENTS", ""),
    "students": ("STUDENTS", ""),
    "humanitarian": ("PEOPLE", "Humanitarian"),
    "animals": ("ANIMALS", ""),
    "emergency": ("LIVES", "Emergency"),
}
UNITS = {"million": "M", "k": "K", "billion": "B"}
COUNTER_RE = re.compile(
    r'data-counter-end="([\d.]+)"[^>]*>[^<]*</span>\s*<span class="gdlr-core-counter-item-suffix">([^<]*)</span>'
    r'.*?<b[^>]*>([^<]*)</b>\s*<br>\s*<p[^>]*>([^<]*)</p>', re.S)


def _display(end, suffix):
    """'42' + '.00+ Million' -> '42M+'; '500' + 'K+' -> '500K+'; '8' + '.90+ Million' -> '8.9M+'."""
    m = re.match(r"\s*(\.\d+)?\s*\+?\s*([A-Za-z]+)\s*\+?\s*$", suffix)
    if not m or m.group(2).lower() not in UNITS:
        raise ValueError(f"unreadable counter suffix {suffix!r}")
    value = float(end + (m.group(1) or ""))
    num = f"{value:.2f}".rstrip("0").rstrip(".")
    return f"{num}{UNITS[m.group(2).lower()]}+", value


def _fetch():
    req = urllib.request.Request(SOURCE, headers={"User-Agent": "Mozilla/5.0 (SRLC USA site build)"})
    html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
    found = {}
    for end, suffix, label, caption in COUNTER_RE.findall(html):
        for key, (want, word) in COUNTERS.items():
            if key not in found and label.strip().upper() == want and word.lower() in caption.lower():
                found[key] = _display(end, suffix)
                break
    missing = set(COUNTERS) - set(found)
    if missing:
        raise ValueError(f"counters not found on {SOURCE}: {', '.join(sorted(missing))}")
    return found


def _load():
    cached = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    if os.environ.get("SRLC_STATS_OFFLINE") == "1":
        return {k: v["display"] for k, v in cached.items()}
    try:
        live = _fetch()
        # a figure that falls by more than half is a misread, not news
        for key, (_, value) in live.items():
            old = cached.get(key, {}).get("value")
            if old and value < old * 0.5:
                raise ValueError(f"{key} dropped from {old} to {value}")
    except Exception as e:  # network down, layout changed, bad value
        print(f"stats: keeping cached figures ({e})", file=sys.stderr)
        return {k: v["display"] for k, v in cached.items()}
    fresh = {k: {"display": d, "value": v} for k, (d, v) in live.items()}
    if fresh != cached:
        with open(CACHE, "w") as f:
            json.dump(fresh, f, indent=2)
            f.write("\n")
        print("stats: updated from " + SOURCE + ": " + ", ".join(f"{k} {d}" for k, (d, _) in live.items()), file=sys.stderr)
    return {k: d for k, (d, _) in live.items()}


_S = _load()
LIVES = _S["lives"]
PATIENTS = _S["patients"]
STUDENTS = _S["students"]
HUMANITARIAN = _S["humanitarian"]
ANIMALS = _S["animals"]
EMERGENCY = _S["emergency"]
