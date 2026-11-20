// gta6-meme-x-01 entry (Node 22, standard library only).
//
// The entry is the X post itself: this program's only job is to hand the gate
// the post's address. It reads POST.json from the repository root and writes
// it to /output/POST.json, where the house reads it and then reads the post
// from X (its first picture and its text) and hands that to the judge.
// Nothing this program writes about the post is judged.
//
// The POST.json shipped here holds a placeholder address, so the gate refuses
// it as it stands. The post's real address goes in once Wilman posts the meme
// from @nodepaar.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const source = join(BOT_DIR, "POST.json");
const target = join(OUTPUT_DIR, "POST.json");

let post: string;
try {
  post = readFileSync(source, "utf8");
} catch (err) {
  console.error(`POST.json could not be read from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}

JSON.parse(post); // the gate needs a JSON object naming an X post's address

mkdirSync(OUTPUT_DIR, { recursive: true });
writeFileSync(target, post);
