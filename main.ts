// news-image-20261118 -- copy the generated front page to the output dir.
// Node 22 stdlib only. No network. The image is produced by gen_image.py;
// this script only copies entry.png to /output/entry.png (or to the
// directory named by MAKEFUN_OUTPUT_DIR when that variable is set).
// Run: node main.ts  (after: python3 gen_image.py)

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, "entry.png"));
