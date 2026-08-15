# Deep-dive — `chrysa/pre-commit-hooks-changelog`

## What it does (1 phrase)

A `pre-commit` hook + standalone CLI (`generate-changelog`) that aggregates a folder of
per-version YAML files (`changelog/*.yaml`, keys: `added / fixed / modified / removed /
upgraded / todo / …`) into a Markdown changelog, with rebuild strategies (`all / versions /
latest / home`).

## Local structure (read)

- `pre_commit_hook/generate_changelog.py` — argparse CLI + `Collect` dataclass: globs
  `changelog/*.yaml`, loads with `ruamel.yaml`, `validate_keys()` against a fixed allow-list
  (`CHANGELOG_ENTRY_AVAILABLE`), fills `content[file.name] = parsed`.
- `pre_commit_hook/formatter.py` (247 l) — `Formatter` dataclass with a `_REBUILD_STRATEGIES`
  dispatch dict (strategy pattern), renders Markdown, writes archive files + home changelog.
- `pre_commit_hook/helper.py` — Markdown rendering helpers.
- `.pre-commit-hooks.yaml` — declares `id: generate-changelog`, `language: python`,
  `files: ^(changelog|changelogs)/.*\.(yml|yaml)$`.
- License: **MIT**. Published to PyPI. Core dep: `ruamel.yaml`.

**Verdict on external refs:** This is a small internal tooling lib, BUT the "changelog from a
folder of fragment files" pattern is a well-established OSS category (fragment/news-file
changelog tooling). Four references are directly on-point and worth a teardown; a fifth
(git-cliff) is the *opposite* philosophy (git-history-driven) and is included as a contrast.

---

## twisted/towncrier — the canonical fragment-changelog tool

- **owner/repo:** twisted/towncrier
- **stars:** ~914
- **activity:** active (1000+ commits, maintained under the Twisted org)
- **language:** Python
- **licence:** **MIT** — ✅ copiable / vendorable
- **pattern file/module:** `src/towncrier/_builder.py` (fragment discovery + grouping),
  `_project.py`, and the `pyproject.toml` `[tool.towncrier]` config schema.
- **mechanism:** Developers drop one file per change into a `newsfragments/` dir, named
  `<issue>.<type>` (e.g. `1234.feature`, `1235.bugfix`). At release, towncrier reads all
  fragments, groups by *type* (feature/bugfix/doc/removal/misc — configurable), renders through
  a Jinja2 template into the top of a `NEWS.rst`/`CHANGELOG` file, then deletes the fragments.
  Its whole reason to exist: **avoid merge conflicts** on a shared changelog file — exactly the
  problem this chrysa repo solves with per-version YAML instead of per-fragment files.
- **portable snippet (config — the fragment-type taxonomy, directly maps to `CHANGELOG_ENTRY_AVAILABLE`):**
  ```toml
  [tool.towncrier]
  directory = "changelog"
  filename = "CHANGELOG.md"
  [[tool.towncrier.type]]
  directory = "added"
  name = "Added"
  showcontent = true
  [[tool.towncrier.type]]
  directory = "fixed"
  name = "Fixed"
  showcontent = true
  ```
- **integration steps:** (1) Adopt towncrier's *config-driven* entry-type taxonomy — replace the
  hardcoded `CHANGELOG_ENTRY_AVAILABLE` list in `generate_changelog.py` with a
  `[tool.changelog]` table in `pyproject.toml` so users add categories without editing code.
  (2) Steal the Jinja2 template rendering to replace the hand-rolled Markdown in
  `helper.py`/`formatter.py` — far more flexible than string concatenation.
  (3) Adopt the "fragment consumed + deleted on release" lifecycle as a rebuild option.
- **gotchas:** towncrier is *fragment-per-change* (many small files), whereas chrysa is
  *file-per-version* (one YAML per release). Don't blindly copy the delete-on-build behavior —
  chrysa's YAML files are the durable source of truth and must survive. Also towncrier renders
  RST-first; Markdown support is there but templates assume RST idioms.

---

## nedbat/scriv — fragment collection with GitHub release sync

- **owner/repo:** nedbat/scriv (Ned Batchelder)
- **stars:** ~304
- **activity:** active (~600 commits)
- **language:** Python
- **licence:** **Apache-2.0** — ✅ copiable (keep NOTICE/attribution)
- **pattern file/module:** `src/scriv/collect.py` (`scriv collect`), `src/scriv/create.py`,
  `src/scriv/format_md.py` + `format_rst.py` (pluggable Markdown/RST formatters).
- **mechanism:** `scriv create` writes a timestamped+branch-named fragment into `changelog.d/`;
  `scriv collect` aggregates them into a `CHANGELOG.md` entry and can then
  `scriv github-release` to push the collected section to a GitHub Release. Cleanly separates
  *format* (md vs rst) behind a formatter abstraction — the same split chrysa has between
  `Formatter` and `Helper`.
- **portable snippet (the Markdown formatter shape worth mirroring):**
  ```python
  # format_md.py concept: sections keyed by category, each a bulleted list
  def format_sections(sections: dict[str, list[str]]) -> str:
      out = []
      for title, items in sections.items():
          out.append(f"### {title}\n")
          out.extend(f"- {line}" for line in items)
          out.append("")
      return "\n".join(out)
  ```
- **integration steps:** (1) Add a `scriv github-release`-style subcommand to publish the
  `latest` rebuild output to a GitHub Release (chrysa already runs on GitHub Actions).
  (2) Adopt scriv's formatter-per-output-format registry if RST/HTML output is ever wanted.
- **gotchas:** Apache-2.0 requires preserving the license header/NOTICE when copying code
  verbatim — fine since chrysa is MIT (Apache→MIT combination is permissible, just attribute).
  scriv assumes fragments carry their own category headers *inside* the file; chrysa keys
  categories at the YAML top level — a structural mismatch, port the idea not the parser.

---

## openstack/reno — YAML release notes, the closest data-model match

- **owner/repo:** openstack/reno (GitHub mirror of OpenStack's repo)
- **stars:** ~62 (low stars because it lives on OpenStack Gerrit, not GitHub-native)
- **activity:** maintained (OpenStack release tooling, still shipped)
- **language:** Python
- **licence:** **Apache-2.0** — ✅ copiable (attribute)
- **pattern file/module:** `reno/scanner.py` (git-tag→note association), `reno/loader.py`
  (loads YAML notes), and the note schema: **each note is a YAML file** with keys like
  `features`, `fixes`, `upgrade`, `deprecations`, `security` — *nearly identical* to chrysa's
  `added/fixed/upgraded/removed`.
- **mechanism:** `reno new` creates a uniquely-named YAML note in `releasenotes/notes/`; at
  build time `reno report` scans **git history/tags** to bucket each note into the release it
  landed in, then renders per-version sections. Key idea chrysa lacks: **git-tag-driven version
  assignment** instead of relying on the YAML filename (`v0.2.0.yaml`).
- **portable snippet (YAML note schema — validate against this exact key set):**
  ```yaml
  features:
    - Added the foobar feature.
  upgrade:
    - The default for X changed to Y.
  fixes:
    - Fixed crash when Z was empty.
  security:
    - Patched CVE-1234.
  ```
- **integration steps:** (1) Add `security` and `deprecations` to `CHANGELOG_ENTRY_AVAILABLE`
  to align with the reno/Keep-a-Changelog superset. (2) Optionally offer a `--from-git` mode
  that derives the version bucket from the nearest git tag (reno's `scanner.py` approach) so a
  single `changelog/unreleased/*.yaml` fragment dir can replace the manual `vX.Y.Z.yaml` naming.
- **gotchas:** reno's git scanner is heavy (walks the full history, needs a real git repo with
  tags) — overkill for a pre-commit hook that must run fast on each commit. Port only the YAML
  schema/validation, keep chrysa's cheap filename-based versioning for the hook path.

---

## orhun/git-cliff — CONTRAST: git-history-driven, not fragment-driven

- **owner/repo:** orhun/git-cliff
- **stars:** ~12.1k
- **activity:** very active (1500+ commits)
- **language:** Rust
- **licence:** **MIT OR Apache-2.0** (dual) — ✅ copiable, but Rust so no direct code reuse
- **pattern file/module:** `config/cliff.toml` (Tera template + commit parsers). Note: **this
  chrysa repo already ships a `cliff.toml`** — so git-cliff is already a known reference here.
- **mechanism:** Parses git history via Conventional Commits + regex parsers, groups commits,
  renders through a Tera template. It is the *opposite* philosophy to this project: git-cliff
  derives the changelog from commit messages; chrysa derives it from hand-authored YAML intent.
- **portable snippet (the template idea — declarative grouping, applicable to chrysa's renderer):**
  ```toml
  [changelog]
  body = """
  {% for group, commits in commits | group_by(attribute="group") %}
  ### {{ group }}
  {% for c in commits %}- {{ c.message }}{% endfor %}
  {% endfor %}
  """
  ```
- **integration steps:** Keep the two as complementary modes — a `--from-git` flag (see reno)
  could shell out to `git-cliff` for the commit-derived section while chrysa YAML supplies the
  curated section. Or simply adopt git-cliff's Tera/Jinja templating philosophy for output.
- **gotchas:** Rust — no code copy possible, pattern-only. Conventional-commit derivation is
  noisy vs. chrysa's curated YAML; don't replace the YAML source of truth with commit scraping.

---

## Cross-cutting takeaways

1. **Externalize the taxonomy:** towncrier + reno both make the entry-category list
   config-driven (`pyproject.toml`). chrysa hardcodes `CHANGELOG_ENTRY_AVAILABLE` — the single
   highest-value borrow. Add `security`/`deprecations` to match Keep-a-Changelog.
2. **Template the render:** replace string-built Markdown in `helper.py`/`formatter.py` with a
   Jinja2/Tera template (towncrier/scriv/git-cliff all do). Cleaner, user-overridable output.
3. **Optional git-tag versioning** (reno) and **GitHub Release sync** (scriv) are natural next
   features; both are permissively licensed and safe to port.

**Licence flags:** all four references are permissive (MIT: towncrier, git-cliff; Apache-2.0:
scriv, reno; git-cliff dual MIT/Apache). **No copyleft/restrictive source** — everything here
is copiable (Apache-2.0 just needs attribution/NOTICE). No GPL/AGPL/BSL/FSL/fair-code involved.
