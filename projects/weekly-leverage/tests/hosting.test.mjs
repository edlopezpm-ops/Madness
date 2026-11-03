// (kommiBo) Publication boundary and failure behavior, using disposable copies only.
import test from "node:test";
import assert from "node:assert/strict";
import {
  mkdtemp,
  mkdir,
  readFile,
  writeFile,
  cp,
  rm,
  readdir,
  symlink,
  rename,
} from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const source = fileURLToPath(new URL("../", import.meta.url));

async function fixture(action) {
  const root = await mkdtemp(join(tmpdir(), "weekly-publication-"));
  try {
    await cp(source, root, {
      recursive: true,
      filter: (path) =>
        !path.includes("/hosting/dist") && !path.includes("/hosting/.wrangler"),
    });
    await action(root);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
}

function build(root) {
  return spawnSync(process.execPath, ["hosting/build.mjs"], {
    cwd: root,
    encoding: "utf8",
  });
}

test("publication contains only public site assets under the dedicated path and native headers", async () => {
  await fixture(async (root) => {
    const result = build(root);
    assert.equal(result.status, 0, result.stderr);
    const dist = join(root, "hosting/dist");
    assert.deepEqual((await readdir(dist)).sort(), [
      "_headers",
      "weekly-leverage",
    ]);
    const files = await readdir(join(dist, "weekly-leverage"));
    assert.equal(files.length, 12); // Ten top-level files, prompt files and locale directories.
    assert.ok(
      !files.includes("README.md") &&
        !files.includes("hosting") &&
        !files.includes("tests"),
    );
    for (const language of ["es", "pt"]) {
      assert.deepEqual(
        await readFile(
          join(
            dist,
            "weekly-leverage/locales/" +
              language +
              "/prompts/01-plan-my-week.txt",
          ),
        ),
        await readFile(
          join(root, "locales/" + language + "/prompts/01-plan-my-week.txt"),
        ),
      );
    }
    assert.ok(
      !files.includes("weekly-leverage-prompts.zip") &&
        !files.includes("USE-NOTES.txt") &&
        !files.includes("favicon.svg"),
    );
    assert.deepEqual(
      await readFile(join(dist, "weekly-leverage/app.js")),
      await readFile(join(root, "app.js")),
    );
    assert.match(
      await readFile(join(dist, "_headers"), "utf8"),
      /form-action 'none'/,
    );
    assert.match(
      await readFile(join(dist, "_headers"), "utf8"),
      /Cache-Control: public, max-age=300, no-transform/,
    );
  });
});

test("unexpected publication material is rejected and left intact for operator inspection", async () => {
  await fixture(async (root) => {
    const dist = join(root, "hosting/dist");
    await mkdir(dist, { recursive: true });
    await writeFile(
      join(dist, "unintended-private-note.txt"),
      "synthetic private fixture",
    );
    const result = build(root);
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /Unexpected file in publication output/);
    assert.equal(
      await readFile(join(dist, "unintended-private-note.txt"), "utf8"),
      "synthetic private fixture",
    );
  });
});

test("publication refuses a symlinked source asset", async () => {
  await fixture(async (root) => {
    await rm(join(root, "app.js"));
    await symlink(join(root, "README.md"), join(root, "app.js"));
    const result = build(root);
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /Expected a regular in-scope source asset/);
  });
});

test("publication refuses a symlinked source parent directory", async () => {
  await fixture(async (root) => {
    await rename(join(root, "prompts"), join(root, "outside-prompts"));
    await symlink(join(root, "outside-prompts"), join(root, "prompts"));
    const result = build(root);
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /Expected a regular in-scope source asset/);
  });
});

test("publication refuses a symlinked output root without writing into it", async () => {
  await fixture(async (root) => {
    const outside = join(root, "outside-output");
    await mkdir(outside);
    await symlink(outside, join(root, "hosting/dist"));
    const result = build(root);
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /Refusing publication directory/);
    assert.deepEqual(await readdir(outside), []);
  });
});

test("manifest cannot turn an unrelated source file into a public prompt", async () => {
  await fixture(async (root) => {
    await writeFile(
      join(root, "PRIVATE-NOTE.txt"),
      "synthetic private fixture",
    );
    const prompts = JSON.parse(
      await readFile(join(root, "prompts.json"), "utf8"),
    );
    prompts[0].file = "../PRIVATE-NOTE.txt";
    await writeFile(join(root, "prompts.json"), JSON.stringify(prompts));
    const result = build(root);
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /does not match the six reviewed filenames/);
  });
});

test("publication refuses a symlinked header input before copying its contents", async () => {
  await fixture(async (root) => {
    const synthetic = join(root, "outside-headers.txt");
    await writeFile(
      synthetic,
      "/weekly-leverage/*\n  X-Fixture-Private: synthetic\n",
    );
    await rm(join(root, "hosting/_headers"));
    await symlink(synthetic, join(root, "hosting/_headers"));
    const result = build(root);
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /Expected a regular in-scope source asset/);
  });
});
