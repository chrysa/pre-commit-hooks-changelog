"""Behavioural tests raising coverage of the changelog generator to the 85% gate.

The three modules were under-covered on develop: generate_changelog.py (Collect +
the argparse main), formatter.py (the rebuild strategies and the home/history/archive
writers) and helper.py (markdown building and its type guards). These tests drive each
on throwaway repos under tmp_path, with the same GIVEN/WHEN/THEN style as the suite.
"""

from pathlib import Path

import pytest

from pre_commit_hook import Collect, Formatter
from pre_commit_hook.generate_changelog import CHANGELOG_ENTRY_AVAILABLE, main
from pre_commit_hook.helper import Helper


# ── fixtures ────────────────────────────────────────────────────────────────────────────


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A repo with a changelog/ folder holding two version files."""
    folder = tmp_path / "changelog"
    folder.mkdir()
    (folder / "0.1.0.yaml").write_text("added:\n  - first feature\n", encoding="utf-8")
    (folder / "0.2.0.yaml").write_text(
        "added:\n  - second feature\nfixed:\n  - a bug\n", encoding="utf-8"
    )
    return tmp_path


def _collect(repo: Path) -> Collect:
    collect = Collect(changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE)
    collect.project_path = repo
    return collect


# ── Collect ─────────────────────────────────────────────────────────────────────────────


class TestCollect:
    def test_versions_files_sorted(self, repo: Path) -> None:
        collect = _collect(repo)
        names = [p.name for p in collect.versions_files]
        assert names == ["0.1.0.yaml", "0.2.0.yaml"]

    def test_collect_versions_reads_all(self, repo: Path) -> None:
        collect = _collect(repo)
        collect.collect_versions()
        assert set(collect.content) == {"0.1.0.yaml", "0.2.0.yaml"}
        assert collect.content["0.2.0.yaml"]["fixed"] == ["a bug"]

    def test_missing_folder_raises(self, tmp_path: Path) -> None:
        collect = _collect(tmp_path)  # no changelog/ dir
        with pytest.raises(NotADirectoryError):
            _ = collect.changelog_folder_path

    def test_archive_path_under_folder(self, repo: Path) -> None:
        collect = _collect(repo)
        assert collect.changelog_folder_archive_path == repo / "changelog" / "archives"

    def test_validate_keys_rejects_unknown(self, repo: Path) -> None:
        collect = _collect(repo)
        collect.chang = {"added": ["x"], "bogus": ["y"]}
        with pytest.raises(ValueError, match="bogus"):
            collect.validate_keys(file_name="0.1.0.yaml")

    def test_validate_keys_accepts_known(self, repo: Path) -> None:
        collect = _collect(repo)
        collect.chang = {"added": ["x"], "fixed": ["y"]}
        collect.validate_keys(file_name="ok.yaml")  # no raise


# ── main (argparse entry point) ─────────────────────────────────────────────────────────


class TestMain:
    def test_main_generates_changelog(self, repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(repo)
        monkeypatch.setattr("sys.argv", ["generate-changelog"])
        assert main() == 0
        assert (repo / "changelog.md").exists()
        assert (repo / "changelog" / "archives").is_dir()

    def test_main_empty_folder_returns_zero(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        (tmp_path / "changelog").mkdir()
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr("sys.argv", ["generate-changelog"])
        assert main() == 0
        assert not (tmp_path / "changelog.md").exists()


# ── Formatter strategies ────────────────────────────────────────────────────────────────


def _content_dict() -> dict:
    return {
        "0.1.0.yaml": {"added": ["first feature"]},
        "0.2.0.yaml": {"added": ["second feature"], "fixed": ["a bug"]},
    }


class TestFormatter:
    def test_generate_default_writes_home_and_archives(self, tmp_path: Path) -> None:
        fmt = Formatter(changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE)
        archives = tmp_path / "changelog" / "archives"
        home = tmp_path / "changelog.md"
        fmt.generate(archives_path=archives, changelog_path=home, content_dict=_content_dict())
        assert home.exists()
        assert (archives / "0.1.0.md").exists()
        assert (archives / "0.2.0.md").exists()
        # home carries the latest version title and a History section (>1 version)
        text = home.read_text(encoding="utf-8")
        assert "0.2.0" in text
        assert "History" in text

    def test_generate_single_version_has_no_history(self, tmp_path: Path) -> None:
        fmt = Formatter(changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE)
        archives = tmp_path / "changelog" / "archives"
        home = tmp_path / "changelog.md"
        fmt.generate(
            archives_path=archives,
            changelog_path=home,
            content_dict={"0.1.0.yaml": {"added": ["only"]}},
        )
        assert "History" not in home.read_text(encoding="utf-8")

    def test_rebuild_versions_only(self, tmp_path: Path) -> None:
        fmt = Formatter(changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE)
        archives = tmp_path / "changelog" / "archives"
        home = tmp_path / "changelog.md"
        fmt.generate(archives_path=archives, changelog_path=home, content_dict=_content_dict(), rebuild="versions")
        assert (archives / "0.2.0.md").exists()
        assert not home.exists()  # "versions" does not write the home file

    def test_rebuild_latest(self, tmp_path: Path) -> None:
        fmt = Formatter(changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE)
        archives = tmp_path / "changelog" / "archives"
        home = tmp_path / "changelog.md"
        # seed archives + home first
        fmt.generate(archives_path=archives, changelog_path=home, content_dict=_content_dict())
        fmt.generate(archives_path=archives, changelog_path=home, content_dict=_content_dict(), rebuild="latest")
        assert (archives / "0.2.0.md").exists()
        assert home.exists()

    def test_rebuild_all_clears_then_regenerates(self, tmp_path: Path) -> None:
        fmt = Formatter(changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE)
        archives = tmp_path / "changelog" / "archives"
        home = tmp_path / "changelog.md"
        fmt.generate(archives_path=archives, changelog_path=home, content_dict=_content_dict())
        stale = archives / "9.9.9.md"
        stale.write_text("stale", encoding="utf-8")
        fmt.generate(archives_path=archives, changelog_path=home, content_dict=_content_dict(), rebuild="all")
        assert not stale.exists()  # remove_archives wiped it
        assert (archives / "0.1.0.md").exists()

    def test_remove_home_and_archives(self, tmp_path: Path) -> None:
        fmt = Formatter(changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE)
        archives = tmp_path / "changelog" / "archives"
        home = tmp_path / "changelog.md"
        fmt.generate(archives_path=archives, changelog_path=home, content_dict=_content_dict())
        fmt.remove_home_changelog(changelog_path=home)
        fmt.remove_archives(archives_path=archives)
        assert not home.exists()
        assert not archives.exists()

    def test_generate_history_empty_without_archives(self, tmp_path: Path) -> None:
        fmt = Formatter(changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE)
        assert fmt.generate_history(archives_path=tmp_path / "nope", latest_version="0.1.0") == ""

    def test_compare_content_true_after_write(self, tmp_path: Path) -> None:
        fmt = Formatter(changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE)
        archives = tmp_path / "changelog" / "archives"
        home = tmp_path / "changelog.md"
        fmt.generate(archives_path=archives, changelog_path=home, content_dict={"0.1.0.yaml": {"added": ["x"]}})
        # a second default generate over identical content hits the SKIPPED branch
        fmt.generate(archives_path=archives, changelog_path=home, content_dict={"0.1.0.yaml": {"added": ["x"]}})
        assert home.exists()


# ── Helper ──────────────────────────────────────────────────────────────────────────────


class TestHelper:
    def test_title(self) -> None:
        assert Helper().title("my version") == "# My Version\n\n"

    def test_add_header_returns_content_with_level(self) -> None:
        helper = Helper()
        out = helper.add_header(value="history", level=2)
        assert out == "## History"

    def test_add_header_no_level_returns_none(self) -> None:
        helper = Helper()
        assert helper.add_header(value="section") is None
        assert "Section" in helper.content

    def test_add_unordered_list(self) -> None:
        assert Helper.add_unordered_list(["a", "b"]) == "\n* a\n* b\n"

    def test_add_unordered_list_rejects_non_str(self) -> None:
        with pytest.raises(TypeError):
            Helper.add_unordered_list([123])  # type: ignore[list-item]

    def test_internal_link(self) -> None:
        assert Helper.internal_link(target="archives/0.1.0.md", display="0.1.0") == "[0.1.0](archives/0.1.0.md)"

    def test_gen_content_dict_with_known_key(self) -> None:
        helper = Helper(changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE)
        out = helper.gen_content(content={"added": ["one", "two"]})
        assert "Added" in out
        assert "* one" in out and "* two" in out

    def test_gen_content_rejects_unsupported_type(self) -> None:
        helper = Helper(changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE)
        with pytest.raises(TypeError):
            helper.gen_content(content=123)  # type: ignore[arg-type]

    def test_gen_content_raises_beyond_max_level(self) -> None:
        helper = Helper(changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE)
        helper.level = Helper.MAX_HEADER_LEVEL + 1
        with pytest.raises(ValueError, match="header levels"):
            helper.gen_content(content={"nested": {"deeper": ["x"]}})

    def test_reset(self) -> None:
        helper = Helper()
        helper.level = 4
        helper.content = "stuff"
        helper.reset()
        assert helper.level == 1 and helper.content == ""
