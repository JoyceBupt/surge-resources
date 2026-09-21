"""Remove the white matte from the user-supplied COX icon (requires Pillow)."""
from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
source = Image.open(ROOT / "sources/cox-round.png").convert("RGB")
pixels = [source.getpixel((x, y)) for y in range(source.height)
          for x in range(source.width)]

# The colored mark has a near-zero red channel. White matte pixels have all
# channels near 255; restrict unmatting to their immediate neighborhood so
# the original gradient away from the boundary stays byte-for-byte intact.
background = Image.new("L", source.size)
background.putdata([255 if min(rgb) >= 248 else 0 for rgb in pixels])
expanded = background.filter(ImageFilter.MaxFilter(9))
boundary = [expanded.getpixel((x, y)) for y in range(source.height)
            for x in range(source.width)]
result = []
for rgb, near_background in zip(pixels, boundary):
    white = min(rgb)
    if white >= 248:
        result.append((0, 0, 0, 0))
    elif near_background and white > 0:
        alpha = 255 - white
        color = tuple(round(255 * (channel - white) / alpha) for channel in rgb)
        result.append((*color, alpha))
    else:
        result.append((*rgb, 255))

output = Image.new("RGBA", source.size)
output.putdata(result)
width, height = output.size
for point in [(0, 0), (width - 1, 0), (0, height - 1),
              (width - 1, height - 1), (width // 2, height // 2)]:
    assert output.getpixel(point)[3] == 0, f"Background is not transparent: {point}"
for before, after, near_background in zip(pixels, result, boundary):
    if not near_background:
        assert after == (*before, 255), "Interior color changed"

destination = ROOT / "icons/cox-round-transparent.png"
output.save(destination, optimize=True)
print(f"Saved {destination}: {width}x{height}, RGBA")
