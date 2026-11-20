import { copyFile, mkdir } from 'node:fs/promises';
import { resolve } from 'node:path';

// news-image-20261120 r2 — graded entrypoint: copy the pre-rendered
// entry.png (built offline by draw.py, PIL) into the grader output dir.
// No dependencies, no network, no rendering at grade time — the image
// the grader scores is byte-identical to the committed entry.png, so the
// run is deterministic by construction (same input bytes, same output).
const out = resolve(process.env.MAKEFUN_OUTPUT_DIR || 'out');
const src = new URL('./entry.png', import.meta.url);
await mkdir(out, { recursive: true });
await copyFile(src, resolve(out, 'entry.png'));
