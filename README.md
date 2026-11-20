# GTA 6 loading screen — a make.fun meme

A GTA 6 meme for make.fun's `gta6-meme-x-01` bounty ($500, top 50 share it).
The joke is the thirteen-year wait: the make.fun ghost has been floating over
a Vice City beach at sunset since 2013, a game controller still waiting on its
towel, the loading bar stuck at 99%.

## The meme

- `meme.png` — the meme, 1080x1080. Built by `composite.py` from the two
  files in `assets/`.
- `meme-480.png` — the same picture at 480x480, the size the judge sees for
  a square image. The ghost, the top line and the loading bar all stay
  readable at that size.
- `assets/scene.png` — the Vice City beach sunset, AI-generated in-session
  (no text, no people, no Rockstar artwork).
- `assets/ghost-mark-1024.png` — make.fun's own ghost mark, from the press
  kit at https://make.fun/press/ (the white ghost with sparkle eyes holding
  its magenta star coin, on its magenta disc). It is composited into the
  scene as a character — floating over the beach with a warm sunset glow
  behind it — not pasted on as a corner sticker.
- `composite.py` — the build script: places the ghost, adds the glow, draws
  the "LOADING GTA VI…" line and the "99% — 13 YEARS AND COUNTING" loading
  bar, exports `meme.png` and `meme-480.png`. Run it with `python3 composite.py`.

## The post

`CAPTION.md` holds the post's text exactly as posted: the joke first, then
the line that on make.fun people and their AI agents earn real money, then
the bounty link, `@makefunai`, and the play code `makefun-inkwell-flask-noodle`
(code 0, verified from the API — never the referral code).

Wilman posts the meme from `@nodepaar` on X. Once it is up, its address goes
into `POST.json` as `{"url": "https://x.com/<handle>/status/<id>"}` and the
entry is submitted.

## The entry program

`main.ts` (Node 22, standard library only) reads `POST.json` from the
repository root and writes it to `/output/POST.json`. That is all it does —
the house reads the post itself from X. Run it locally with:

    mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

## License

MIT. See `LICENSE`.
