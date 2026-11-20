"""Build the gta6-meme-x-01 meme: composite make.fun's press-kit ghost into a
generated Vice City beach sunset, add the loading-screen joke, export square.

Inputs (all in assets/ next to this script):
  scene.png            - AI-generated Vice City beach sunset (1600x1600, no text)
  ghost-mark-1024.png  - make.fun press-kit ghost mark (1024x1024 RGBA)
Output:
  meme.png             - final meme, 1080x1080
  meme-480.png         - 480x480 preview (what the judge sees for a square)

The ghost is a character in the scene, not a corner sticker: it floats over the
beach with a warm sunset glow behind it, above the game controller waiting on
its towel.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

CANVAS = 1600          # work at the scene's native size, downscale at the end
OUT = 1080             # final square
MAGENTA = (196, 28, 131)   # the ghost disc's magenta, sampled from the mark

TOP_TEXT = "LOADING GTA VI\u2026"
BAR_TEXT = "99% \u2014 13 YEARS AND COUNTING"


def load_font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size)


def radial_glow(radius: int, color, max_alpha: int) -> Image.Image:
    """A smooth radial glow: concentric circles fading to transparent, so the
    falloff is gradual and never reads as a plate with an edge."""
    size = radius * 2
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    steps = 64
    for i in range(steps, 0, -1):
        r = radius * i / steps
        a = int(max_alpha * (1 - i / steps) ** 2)
        draw.ellipse(
            (radius - r, radius - r, radius + r, radius + r),
            fill=color + (a,),
        )
    return layer


def main() -> None:
    scene = Image.open(ASSETS / "scene.png").convert("RGB")
    assert scene.size == (CANVAS, CANVAS), scene.size
    base = scene.convert("RGBA")

    ghost = Image.open(ASSETS / "ghost-mark-1024.png").convert("RGBA")

    # --- ghost placement: floating over the beach, left of centre so the
    # palms on the right stay clear; big enough to read at 480x480.
    ghost_d = 600
    ghost_cx, ghost_top = 720, 320
    ghost_r = ghost.resize((ghost_d, ghost_d), Image.LANCZOS)
    ghost_cy = ghost_top + ghost_d // 2

    # Warm sunset glow behind the ghost, so it reads as lit by the scene.
    # A true radial gradient (no hard edge); the ghost floats, so it carries
    # no ground shadow — the earlier shadow read as a smudge on the water.
    glow = radial_glow(460, (255, 140, 60), 70)
    base.alpha_composite(glow, (ghost_cx - 460, ghost_cy - 460))

    # The ghost itself.
    base.alpha_composite(ghost_r, (ghost_cx - ghost_d // 2, ghost_top))

    draw = ImageDraw.Draw(base)

    # --- top line: the setup, big white type with a heavy black outline.
    top_font = load_font(102)
    draw.text(
        (CANVAS // 2, 108),
        TOP_TEXT,
        font=top_font,
        fill=(255, 255, 255),
        anchor="ma",
        stroke_width=8,
        stroke_fill=(0, 0, 0),
    )

    # --- loading bar: dark track, magenta fill at 99%, punchline inside it.
    bar_x0, bar_x1 = 300, 1300
    bar_y0, bar_y1 = 1290, 1360
    bar_h = bar_y1 - bar_y0
    draw.rounded_rectangle(
        (bar_x0, bar_y0, bar_x1, bar_y1),
        radius=bar_h // 2,
        fill=(0, 0, 0, 150),
    )
    fill_x1 = bar_x0 + int((bar_x1 - bar_x0) * 0.99)
    draw.rounded_rectangle(
        (bar_x0, bar_y0, fill_x1, bar_y1),
        radius=bar_h // 2,
        fill=MAGENTA + (255,),
    )
    bar_font = load_font(52)
    draw.text(
        (CANVAS // 2, (bar_y0 + bar_y1) // 2),
        BAR_TEXT,
        font=bar_font,
        fill=(255, 255, 255),
        anchor="mm",
        stroke_width=3,
        stroke_fill=(0, 0, 0),
    )

    # --- export: final square + the 480px view the judge sees.
    out = base.convert("RGB").resize((OUT, OUT), Image.LANCZOS)
    out.save(HERE / "meme.png")
    out.resize((480, 480), Image.LANCZOS).save(HERE / "meme-480.png")
    print("wrote meme.png (1080x1080) and meme-480.png (480x480)")


if __name__ == "__main__":
    main()
