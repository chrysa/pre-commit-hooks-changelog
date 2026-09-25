#!/usr/bin/env node
/**
 * pre-commit-self-test.cjs — catch entry-point/schema drift before it merges.
 *
 * This repo IS a pre-commit hook (see `.pre-commit-hooks.yaml`, entry point
 * `generate-changelog`). Unit tests exercise the Python internals, but nothing
 * runs the hook the way a consumer repo's pre-commit actually invokes it —
 * so a broken `entry`/`language`/`args` in `.pre-commit-hooks.yaml`, or a
 * changed CLI contract in `pre_commit_hook/generate_changelog.py`, can slip
 * through.
 *
 * PreToolUse (Bash → git commit): when staged changes touch
 * `pre_commit_hook/**` or `.pre-commit-hooks.yaml`, runs
 * `pre-commit try-repo . generate-changelog --all-files` against this repo
 * itself. Non-zero exit blocks the commit (exit 2) with the failure printed.
 *
 * Best-effort: missing `pre-commit` CLI, or any internal error, exits 0 —
 * this is a fast local guard, not the enforcement of record (CI covers that).
 */
const { execSync } = require("node:child_process");

const BLOCK = 2;
const OK = 0;

function isCommit(input) {
  const command = input?.tool_input?.command;
  return typeof command === "string" && /\bgit\s+commit\b/.test(command);
}

function touchesHookCode(repoRoot) {
  try {
    const staged = execSync("git diff --cached --name-only", {
      cwd: repoRoot,
      encoding: "utf8",
    });
    return staged
      .split("\n")
      .some((path) => path.startsWith("pre_commit_hook/") || path === ".pre-commit-hooks.yaml");
  } catch {
    return false;
  }
}

function main() {
  let input;
  try {
    input = JSON.parse(require("node:fs").readFileSync(0, "utf8"));
  } catch {
    process.exit(OK);
    return;
  }

  const repoRoot = process.env.CLAUDE_PROJECT_DIR || process.cwd();
  if (!isCommit(input) || !touchesHookCode(repoRoot)) {
    process.exit(OK);
    return;
  }

  try {
    execSync("pre-commit --version", { cwd: repoRoot, stdio: "ignore" });
  } catch {
    process.exit(OK); // pre-commit not installed locally — CI is the real gate
    return;
  }

  try {
    execSync("pre-commit try-repo . generate-changelog --all-files", {
      cwd: repoRoot,
      stdio: "pipe",
      timeout: 60000,
    });
    process.exit(OK);
  } catch (error) {
    process.stderr.write(
      `pre-commit-self-test: hook self-check failed — the changelog hook (entry: generate-changelog) ` +
        `no longer runs cleanly against this repo. Fix before committing:\n${error.stdout || error.message}\n`,
    );
    process.exit(BLOCK);
  }
}

main();
