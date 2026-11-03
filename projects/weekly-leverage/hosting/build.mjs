// (kommiBo) Copy only reviewed public assets; no other repository files are deployed.
import {
  mkdir,
  readFile,
  writeFile,
  copyFile,
  readdir,
  lstat,
  realpath,
} from "node:fs/promises";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const hosting = await realpath(dirname(fileURLToPath(import.meta.url)));
const source = resolve(hosting, "..");
const destination = join(hosting, "dist");

async function requireSourceFile(original) {
  if (
    !original.startsWith(source + "/") ||
    !(await lstat(original)).isFile() ||
    (await realpath(original)) !== original
  ) {
    throw new Error(
      "Expected a regular in-scope source asset: " + relative(source, original),
    );
  }
}

await requireSourceFile(join(source, "prompts.json"));
await requireSourceFile(join(hosting, "_headers"));
const prompts = JSON.parse(
  await readFile(join(source, "prompts.json"), "utf8"),
);
const promptFiles = [
  "01-plan-my-week.txt",
  "02-define-the-tasks.txt",
  "03-move-it-to-my-apps.txt",
  "04-start-the-day.txt",
  "05-rebalance-a-disrupted-week.txt",
  "06-close-and-repeat.txt",
];
if (
  !Array.isArray(prompts) ||
  prompts.length !== promptFiles.length ||
  !prompts.every((prompt, index) => prompt.file === promptFiles[index])
) {
  throw new Error("Prompt manifest does not match the six reviewed filenames");
}
const files = [
  "index.html",
  "style.css",
  "app.js",
  "planner.mjs",
  "favicon.svg",
  "social-card.png",
  "aekr-mark.png",
  "prompts.json",
  "USE-NOTES.txt",
  "weekly-leverage-prompts.zip",
  ...promptFiles.map((file) => "prompts/" + file),
];
const allowed = new Set([
  "_headers",
  ...files.map((file) => "weekly-leverage/" + file),
]);

async function existingFiles(directory) {
  const found = [];
  try {
    const directoryInfo = await lstat(directory);
    if (directoryInfo.isSymbolicLink() || !directoryInfo.isDirectory()) {
      throw new Error("Refusing publication directory: " + directory);
    }
    for (const entry of await readdir(directory, { withFileTypes: true })) {
      const path = join(directory, entry.name);
      if (entry.isSymbolicLink())
        throw new Error("Refusing publication symlink: " + path);
      if (entry.isDirectory()) found.push(...(await existingFiles(path)));
      else if (entry.isFile())
        found.push(relative(destination, path).split("\\").join("/"));
      else throw new Error("Refusing unexpected publication entry: " + path);
    }
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
  }
  return found;
}

// Refuse stale/unexpected files instead of publishing or deleting them silently.
for (const file of await existingFiles(destination)) {
  if (!allowed.has(file))
    throw new Error("Unexpected file in publication output: " + file);
}
for (const file of files) {
  const original = resolve(source, file);
  await requireSourceFile(original);
  const output = join(destination, "weekly-leverage", file);
  await mkdir(dirname(output), { recursive: true });
  await copyFile(original, output);
}
await writeFile(
  join(destination, "_headers"),
  await readFile(join(hosting, "_headers")),
);
console.log(
  "Prepared " +
    allowed.size +
    " static publication files for /weekly-leverage/.",
);
