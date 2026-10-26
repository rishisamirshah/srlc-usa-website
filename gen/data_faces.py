"""Face-safe photo crops (Naman, Oct 22, site-wide: no face cut off in any
photo, at any width). Positions are solved by gen/qa (face detection on
the photo + the visible crop of every placement at 1920 to 360 wide), not
set by eye. A string is one object-position everywhere; a dict splits it:
"pos" above 860px, "md" 481 to 860px, "sm" phones (inner-page heroes are a
fixed 39:64 box there). Rendered as --fp / --fp-md / --fp-sm (see
supplement-z-naman.css). Rerun gen/qa after changing a photo or a layout."""

FACE_POS = {
    "/assets/img/mb/mb-105.webp": "54% 36%",
    "/assets/img/mb/mb-158.webp": "54% 50%",
    "/assets/img/mb/mb-159.webp": "28% 24%",
    "/assets/img/mb/mb-160.webp": "16% 50%",
    "/assets/img/mb/mb-167.webp": "40% 18%",
    "/assets/img/mb/mb-172.webp": "54% 50%",
    "/assets/img/mb/mb-176.webp": {"pos": "88% 46%", "md": "34% 46%", "sm": "18% 46%"},
    "/assets/img/mb/mb-195.webp": {"pos": "0% 30%", "md": "40% 26%", "sm": "90% 26%"},
    "/assets/img/mb/mb-208.webp": {"pos": "70% 36%", "md": "82% 42%", "sm": "30% 42%"},
    "/assets/img/mb/mb-209.webp": "50% 50%",
    "/assets/img/mb/mb-306.webp": "88% 22%",
    "/assets/img/mb/mb-319.webp": "30% 50%",
    "/assets/img/mb/mb-332.webp": "50% 38%",
    "/assets/img/mb/mb-334.webp": "58% 14%",
    "/assets/img/mb/mb-339.webp": "50% 44%",
    "/assets/img/mb/mb-354.webp": "44% 36%",
    "/assets/img/mb/mb-355.webp": "50% 50%",
    "/assets/img/mb/mb-357.webp": {"pos": "64% 50%", "md": "50% 50%", "sm": "50% 50%"},
    "/assets/img/mb/mb-360.webp": {"pos": "0% 40%", "md": "100% 24%", "sm": "0% 24%"},
    "/assets/img/mb/mb-395.webp": "82% 50%",
    "/assets/img/mb/mb-399.webp": "50% 34%",
    "/assets/img/mb/mb-404.webp": "50% 10%",
    "/assets/img/mb/mb-433.webp": {"pos": "68% 0%", "md": "36% 20%", "sm": "36% 20%"},
    "/assets/img/mb/mb-436.webp": "50% 34%",
    "/assets/img/mb/mb-443.webp": "30% 44%",
    "/assets/img/mb/mb-445.webp": "50% 38%",
    "/assets/img/mb/mb-454.webp": {"pos": "66% 38%", "md": "96% 42%", "sm": "50% 42%"},
    "/assets/img/mb/mb-458.webp": "48% 22%",
    "/assets/img/mb/mb-463.webp": "10% 50%",
    "/assets/img/mb/mb-464.webp": "98% 50%",
    "/assets/img/mb/mb-491.webp": "50% 42%",
    "/assets/img/mb/mb-497.webp": "84% 50%",
    "/assets/img/mb/mb-515.webp": "50% 48%",
    "/assets/img/mb/mb-519.webp": "24% 44%",
    "/assets/img/mb/mb-619.webp": "50% 48%",
    "/assets/img/mb/mb-627.webp": "50% 16%",
    "/assets/img/mb/mb-703.webp": "74% 50%",
    "/assets/img/mb/mb-714.webp": "44% 50%",
    "/assets/img/mb/mb-716.webp": {"pos": "100% 44%", "md": "100% 42%", "sm": "60% 42%"},
    "/assets/img/mb/mb-720.webp": "76% 94%",
    "/assets/img/mb/mb-721.webp": {"pos": "50% 20%", "md": "82% 20%", "sm": "80% 20%"},
    "/assets/img/mb/mb-81.webp": "50% 42%",
    "/assets/img/mb/mb-82.webp": "44% 28%",
    "/assets/img/mb/mb-84.webp": "82% 24%",
    "/assets/img/mb/mb-92.webp": "54% 36%",
    "/assets/img/naman/care-child-care.webp": "100% 50%",
    "/assets/img/naman/care-community-care.webp": "42% 50%",
    "/assets/img/naman/care-educational-care.webp": "66% 50%",
    "/assets/img/naman/care-tribal-care.webp": "4% 50%",
    "/assets/img/naman/care-woman-care.webp": "62% 50%",
}

# Photos whose crop is picked live in the browser (gen/supplement-zzz-facefit.js)
# because no fixed position keeps every face whole at every width: the page
# measures the photo's real box and picks the position, and a slight zoom if
# needed, that leaves every face fully in or fully out. Who We Are's three
# section photos get this too (story_split mod="wwa").
FACE_FIT = {
    "/assets/img/mb/mb-357.webp",   # Humanitarian Care, Indianapolis sandwich line
    "/assets/img/mb/mb-30.webp",    # Our Impact operating model band, supply-kit table
}

# Heroes framed live above 860px (supplement-zzz-facefit.js): at 900px wide no
# single crop keeps every face whole and clear of the headline (Oct 24 audit).
HERO_FIT = {
    "/assets/img/mb/mb-208.webp",   # Health Care
    "/assets/img/mb/mb-716.webp",   # Events
    "/assets/img/mb/mb-81.webp",    # Center of Excellence for Women
    "/assets/img/mb/mb-721.webp",   # Management Team (headline over faces at short screens)
    "/assets/img/mb/mb-82.webp",    # Woman Care (same)
    "/assets/img/mb/mb-195.webp",   # Our Impact and Child Care crowd, until Naman's new photo
}
