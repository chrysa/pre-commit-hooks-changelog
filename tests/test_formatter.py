import pytest
from pathlib import Path

from pre_commit_hook.formatter import Formatter
from pre_commit_hook.generate_changelog import CHANGELOG_ENTRY_AVAILABLE


@pytest.fixture
def formatter():
    return Formatter(changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE)


@pytest.fixture
def single_version_content():
    return {"v1.0.0.yaml": {"added": ["initial release"]}}


@pytest.fixture
def multi_version_content():
    return {
        "v1.0.0.yaml": {"added": ["initial release"]},
        "v1.1.0.yaml": {"fixed": ["bug fix"], "added": ["new feature"]},
    }


class TestFormatterGenerateDefault:
    def test_creates_home_changelog(self, tmp_path, formatter, multi_version_content):
        archives = tmp_path / "archives"
        changelog = tmp_path / "changelog.md"
        formatter.generate(
            archives_path=archives,
            changelog_path=changelog,
            content_dict=multi_version_content,
        )
        assert changelog.exists()

    def test_creates_version_archives(self, tmp_path, formatter, multi_version_content):
        archives = tmp_path / "archives"
        changelog = tmp_path / "changelog.md"
        formatter.generate(
            archives_path=archives,
            changelog_path=changelog,
            content_dict=multi_version_content,
        )
        assert (archives / "v1.0.0.md").exists()
        assert (archives / "v1.1.0.md").exists()

    def test_creates_archives_directory(self, tmp_path, formatter, multi_version_content):
        archives = tmp_path / "archives"
        changelog = tmp_path / "changelog.md"
        assert not archives.exists()
        formatter.generate(
            archives_path=archives,
            changelog_path=changelog,
            content_dict=multi_version_content,
        )
        assert archives.is_dir()


class TestFormatterVersionContent:
    def test_version_file_contains_title(self, tmp_path, formatter, multi_version_content):
        archives = tmp_path / "archives"
        changelog = tmp_path / "changelog.md"
        formatter.generate(
            archives_path=archives,
            changelog_path=changelog,
            content_dict=multi_version_content,
        )
        content = (archives / "v1.0.0.md").read_text()
        assert "# V1.0.0" in content

    def test_version_file_contains_entries(self, tmp_path, formatter, multi_version_content):
        archives = tmp_path / "archives"
        changelog = tmp_path / "changelog.md"
        formatter.generate(
            archives_path=archives,
            changelog_path=changelog,
            content_dict=multi_version_content,
        )
        content = (archives / "v1.0.0.md").read_text()
        assert "Added" in content
        assert "initial release" in content

    def test_home_changelog_contains_latest_version(self, tmp_path, formatter, multi_version_content):
        archives = tmp_path / "archives"
        changelog = tmp_path / "changelog.md"
        formatter.generate(
            archives_path=archives,
            changelog_path=changelog,
            content_dict=multi_version_content,
        )
        content = changelog.read_text()
        assert "V1.1.0" in content

    def test_home_changelog_has_history_section(self, tmp_path, formatter, multi_version_content):
        archives = tmp_path / "archives"
        changelog = tmp_path / "changelog.md"
        formatter.generate(
            archives_path=archives,
            changelog_path=changelog,
            content_dict=multi_version_content,
        )
        content = changelog.read_text()
        assert "History" in content

    def test_home_changelog_no_history_for_single_version(
        self, tmp_path, formatter, single_version_content
    ):
        archives = tmp_path / "archives"
        changelog = tmp_path / "changelog.md"
        formatter.generate(
            archives_path=archives,
            changelog_path=changelog,
            content_dict=single_version_content,
        )
        content = changelog.read_text()
        assert "History" not in content


class TestFormatterSkipUnchanged:
    def test_skips_unchanged_file(self, tmp_path, multi_version_content, capsys):
        archives = tmp_path / "archives"
        changelog = tmp_path / "changelog.md"
        Formatter(changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE).generate(
            archives_path=archives,
            changelog_path=changelog,
            content_dict=multi_version_content,
        )
        Formatter(changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE).generate(
            archives_path=archives,
            changelog_path=changelog,
            content_dict=multi_version_content,
        )
        captured = capsys.readouterr()
        assert "SKIPPED" in captured.out


class TestFormatterRebuildAll:
    def test_rebuild_all_recreates_everything(self, tmp_path, formatter, multi_version_content):
        archives = tmp_path / "archives"
        changelog = tmp_path / "changelog.md"
        formatter.generate(
            archives_path=archives,
            changelog_path=changelog,
            content_dict=multi_version_content,
        )
        formatter2 = Formatter(changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE)
        formatter2.generate(
            archives_path=archives,
            changelog_path=changelog,
            content_dict=multi_version_content,
            rebuild="all",
        )
        assert changelog.exists()
        assert (archives / "v1.0.0.md").exists()
        assert (archives / "v1.1.0.md").exists()


class TestFormatterRebuildVersions:
    def test_rebuild_versions_creates_archives_only(
        self, tmp_path, formatter, multi_version_content
    ):
        archives = tmp_path / "archives"
        changelog = tmp_path / "changelog.md"
        formatter.generate(
            archives_path=archives,
            changelog_path=changelog,
            content_dict=multi_version_content,
            rebuild="versions",
        )
        assert (archives / "v1.0.0.md").exists()
        assert (archives / "v1.1.0.md").exists()
        assert not changelog.exists()


class TestFormatterRebuildLatest:
    def test_rebuild_latest_creates_latest_archive(
        self, tmp_path, formatter, multi_version_content
    ):
        archives = tmp_path / "archives"
        changelog = tmp_path / "changelog.md"
        formatter.generate(
            archives_path=archives,
            changelog_path=changelog,
            content_dict=multi_version_content,
            rebuild="latest",
        )
        assert (archives / "v1.1.0.md").exists()
        assert changelog.exists()


class TestFormatterRebuildHome:
    def test_rebuild_home_creates_only_home(self, tmp_path, formatter, multi_version_content):
        archives = tmp_path / "archives"
        changelog = tmp_path / "changelog.md"
        formatter.generate(
            archives_path=archives,
            changelog_path=changelog,
            content_dict=multi_version_content,
            rebuild="home",
        )
        assert changelog.exists()
        assert not (archives / "v1.0.0.md").exists()
        assert not (archives / "v1.1.0.md").exists()


class TestFormatterCompareContent:
    def test_compare_returns_true_for_same_content(self, tmp_path, formatter):
        f = tmp_path / "test.md"
        formatter.content = "# Title\n\n* item\n"
        f.write_text("# Title\n\n* item\n")
        assert formatter.compare_content(f) is True

    def test_compare_returns_false_for_different_content(self, tmp_path, formatter):
        f = tmp_path / "test.md"
        formatter.content = "# Title\n\n* new item\n"
        f.write_text("# Title\n\n* old item\n")
        assert formatter.compare_content(f) is False

    def test_compare_returns_false_when_file_missing(self, tmp_path, formatter):
        formatter.content = "# Title\n"
        assert formatter.compare_content(tmp_path / "missing.md") is False

    def test_compare_ignores_trailing_newlines(self, tmp_path, formatter):
        f = tmp_path / "test.md"
        formatter.content = "# Title\n\n* item\n\n\n"
        f.write_text("# Title\n\n* item\n")
        assert formatter.compare_content(f) is True


class TestFormatterRemoveHelpers:
    def test_remove_home_changelog(self, tmp_path):
        changelog = tmp_path / "changelog.md"
        changelog.write_text("content")
        Formatter.remove_home_changelog(changelog_path=changelog)
        assert not changelog.exists()

    def test_remove_home_changelog_missing_file(self, tmp_path):
        # Should not raise
        Formatter.remove_home_changelog(changelog_path=tmp_path / "missing.md")

    def test_remove_archives(self, tmp_path):
        archives = tmp_path / "archives"
        archives.mkdir()
        (archives / "v1.0.0.md").write_text("content")
        Formatter.remove_archives(archives_path=archives)
        assert not archives.exists()

    def test_remove_archives_missing_dir(self, tmp_path):
        # Should not raise
        Formatter.remove_archives(archives_path=tmp_path / "missing")

    def test_remove_version(self, tmp_path):
        archives = tmp_path / "archives"
        archives.mkdir()
        (archives / "v1.0.0.md").write_text("content")
        Formatter.remove_version(archives_path=archives, version="v1.0.0.yaml")
        assert not (archives / "v1.0.0.md").exists()
