"""Interim trustee cards (Oct 29): the live site only has small, mostly
circle-cropped portraits, so each card is the person's photo as a circle at
one size and one eye height on the site's lavender, 3:4. Replace a card's file
with a real portrait (3:4, head to waist) and the page needs no change.
Run from the folder holding the live site's originals (srlcusa.org/wp-content/
uploads: Snehal-Shah.png, Chintan.png, KirtiDesai.png, KaminiShah.jpg,
PayalKamdar.jpg, Lakhani.jpg, BirenMehta.jpg, ChiragShah.png)."""
from PIL import Image, ImageDraw, ImageFilter
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'assets', 'img', 'trustees') + '/'
CW, CH = 720, 960
BG = (237, 229, 245)        # #EDE5F5
D = 480                     # circle diameter
EYE_Y = 455                 # eye line, the same in every card
P = [  # file, out, circle source?, eye x, eye y, head height (shares of the source)
    ('Snehal-Shah.png', 'snehal-shah', True, 0.53, 0.53, 0.82),
    ('Chintan.png', 'chintan-mehta', True, 0.45, 0.45, 0.71),
    ('KirtiDesai.png', 'kirti-desai', False, 0.47, 0.37, 0.52),
    ('KaminiShah.jpg', 'kamini-shah', True, 0.62, 0.50, 0.70),
    ('PayalKamdar.jpg', 'payal-kamdar', False, 0.30, 0.43, 0.67),
    ('Lakhani.jpg', 'mitesh-lakhani', True, 0.50, 0.38, 0.70),
    ('BirenMehta.jpg', 'biren-mehta', False, 0.51, 0.40, 0.56),
    ('ChiragShah.png', 'chirag-shah', False, 0.47, 0.36, 0.52),
]
for f, out, circle, ex, ey, hh in P:
    src = Image.open(f).convert('RGBA'); w, h = src.size
    flat = Image.new('RGBA', src.size, (255, 255, 255, 255)); flat.alpha_composite(src); src = flat.convert('RGB')
    if circle:
        a = 0.015  # inset past the original's anti-aliased edge
        sq = src.crop((round(w * a), round(h * a), round(w * (1 - a)), round(h * (1 - a))))
        eye_in = (ey - a) / (1 - 2 * a)
    else:
        S = min(hh * h / 0.73, w, h)
        cx, cy = ex * w, ey * h
        x0 = min(max(cx - S / 2, 0), w - S); y0 = min(max(cy - 0.45 * S, 0), h - S)
        sq = src.crop((round(x0), round(y0), round(x0 + S), round(y0 + S)))
        eye_in = (cy - y0) / S
    disc = sq.resize((D, D), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1, percent=50, threshold=2))
    m = Image.new('L', (D * 4, D * 4), 0); ImageDraw.Draw(m).ellipse([0, 0, D * 4 - 1, D * 4 - 1], fill=255)
    m = m.resize((D, D), Image.LANCZOS)
    card = Image.new('RGB', (CW, CH), BG)
    card.paste(disc, ((CW - D) // 2, round(EYE_Y - eye_in * D)), m)
    card.save(OUT + out + '.jpg', quality=88, optimize=True, progressive=True)
