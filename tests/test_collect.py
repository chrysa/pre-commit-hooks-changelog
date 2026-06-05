import pytest
from pathlib import Path

from pre_commit_hook.generate_changelog import Collect
from pre_commit_hook.generate_changelog import CHANGELOG_ENTRY_AVAILABLE


class TestCollectPaths:
    def test_default_changelog_folder_path(self, tmp_path, mocker):
        # GIVEN default changelog folder name
        # WHEN access changelog_folder_path
        # THEN returns path to <project>/changelog
        changelog_folder = tmp_path / "changelog"
        changelog_folder.mkdir()
        collect = Collect()
        mocker.patch.object(collect, "project_path", tmp_path)
        assert collect.changelog_folder_path == changelog_folder

    def test_custom_changelog_folder_path(self, tmp_path, mocker):
        # GIVEN custom changelog folder name
        # WHEN access changelog_folder_path
        # THEN returns path to custom folder
        changelog_folder = tmp_path / "my_changelogs"
        changelog_folder.mkdir()
        collect = Collect(changelog_folder="my_changelogs")
        mocker.patch.object(collect, "project_path", tmp_path)
        assert collect.changelog_folder_path == changelog_folder

    def test_changelog_folder_not_found_raises(self, tmp_path, mocker):
        # GIVEN a missing changelog folder
        # WHEN access changelog_folder_path
        # THEN raises NotADirectoryError
        collect = Collect()
        mocker.patch.object(collect, "project_path", tmp_path)
        with pytest.raises(NotADirectoryError):
            _ = collect.changelog_folder_path

    def test_default_changelog_path(self, tmp_path, mocker):
        # GIVEN default output file name
        # WHEN access changelog_path
        # THEN returns path to <project>/changelog.md
        collect = Collect()
        mocker.patch.object(collect, "project_path", tmp_path)
        assert collect.changelog_path == tmp_path / "changelog.md"

    def test_custom_output_file(self, tmp_path, mocker):
        # GIVEN custom output file name
        # WHEN access changelog_path
        # THEN returns path to custom output file
        collect = Collect(main_output_file="CHANGES.md")
        mocker.patch.object(collect, "project_path", tmp_path)
        assert collect.changelog_path == tmp_path / "CHANGES.md"

    def test_archive_path_is_under_changelog_folder(self, tmp_path, mocker):
        # GIVEN default folder names
        # WHEN access changelog_folder_archive_path
        # THEN path is <changelog_folder>/archives
        folder = tmp_path / "changelog"
        folder.mkdir()
        collect = Collect()
        mocker.patch.object(collect, "project_path", tmp_path)
        assert collect.changelog_folder_archive_path == folder / "archives"

    def test_custom_archive_path(self, tmp_path, mocker):
        # GIVEN custom archives subfolder name
        # WHEN access changelog_folder_archive_path
        # THEN path uses the custom name
        folder = tmp_path / "changelog"
        folder.mkdir()
        collect = Collect(archives_path="history")
        mocker.patch.object(collect, "project_path", tmp_path)
        assert collect.changelog_folder_archive_path == folder / "history"


class TestVersionsFiles:
    def test_returns_only_yaml_files(self, tmp_path, mocker):
        folder = tmp_path / "changelog"
        folder.mkdir()
        (folder / "v1.0.0.yaml").write_text("added:\n  - test\n")
        (folder / "v1.1.0.yaml").write_text("fixed:\n  - bug\n")
        (folder / "notes.txt").write_text("ignore me")
        (folder / "archives").mkdir()
        collect = Collect(changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE)
        mocker.patch.object(collect, "project_path", tmp_path)
        files = list(collect.versions_files)
        assert len(files) == 2
        assert all(f.suffix == ".yaml" for f in files)

    def test_returns_list(self, tmp_path, mocker):
        folder = tmp_path / "changelog"
        folder.mkdir()
        collect = Collect()
        mocker.patch.object(collect, "project_path", tmp_path)
        assert isinstance(collect.versions_files, list)


class TestCollectVersions:
    def test_collect_versions_loads_content(self, tmp_path, mocker):
        folder = tmp_path / "changelog"
        folder.mkdir()
        (folder / "v1.0.0.yaml").write_text("added:\n  - feature A\n")
        collect = Collect(changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE)
        mocker.patch.object(collect, "project_path", tmp_path)
        collect.collect_versions()
        assert "v1.0.0.yaml" in collect.content
        assert collect.content["v1.0.0.yaml"] == {"added": ["feature A"]}

    def test_collect_versions_sorted_alphabetically(self, tmp_path, mocker):
        folder = tmp_path / "changelog"
        folder.mkdir()
        (folder / "v1.2.0.yaml").write_text("fixed:\n  - bug\n")
        (folder / "v1.0.0.yaml").write_text("added:\n  - init\n")
        (folder / "v1.1.0.yaml").write_text("upgraded:\n  - dep\n")
        collect = Collect(changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE)
        mocker.patch.object(collect, "project_path", tmp_path)
        collect.collect_versions()
        keys = list(collect.content.keys())
        assert keys == ["v1.0.0.yaml", "v1.1.0.yaml", "v1.2.0.yaml"]

    def test_collect_versions_invalid_key_raises(self, tmp_path, mocker):
        folder = tmp_path / "changelog"
        folder.mkdir()
        (folder / "v1.0.0.yaml").write_text("invalid_section:\n  - entry\n")
        collect = Collect(changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE)
        mocker.patch.object(collect, "project_path", tmp_path)
        with pytest.raises(ValueError, match="invalid_section"):
            collect.collect_versions()

    def test_collect_versions_multiple_files(self, tmp_path, mocker):
        folder = tmp_path / "changelog"
        folder.mkdir()
        (folder / "v1.0.0.yaml").write_text("added:\n  - init\n")
        (folder / "v1.1.0.yaml").write_text("fixed:\n  - bug\n")
        collect = Collect(changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE)
        mocker.patch.object(collect, "project_path", tmp_path)
        collect.collect_versions()
        assert len(collect.content) == 2


class TestValidateKeys:
    def setup_method(self):
        self.collect = Collect(changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE)

    def test_valid_single_key(self):
        self.collect.chang = {"added": ["x"]}
        self.collect.validate_keys(file_name="test.yaml")

    def test_valid_multiple_keys(self):
        self.collect.chang = {"added": ["x"], "fixed": ["y"], "upgraded": ["z"]}
        self.collect.validate_keys(file_name="test.yaml")

    def test_invalid_key_raises_value_error(self):
        self.collect.chang = {"added": ["x"], "oops": ["y"]}
        with pytest.raises(ValueError, match="oops"):
            self.collect.validate_keys(file_name="test.yaml")

    def test_invalid_key_includes_filename_in_message(self):
        self.collect.chang = {"bad_key": ["x"]}
        with pytest.raises(ValueError, match="v1.0.0.yaml"):
            self.collect.validate_keys(file_name="v1.0.0.yaml")

    def test_all_changelog_entries_valid(self):
        self.collect.chang = {entry: ["value"] for entry in CHANGELOG_ENTRY_AVAILABLE}
        self.collect.validate_keys(file_name="test.yaml")

    def test_case_insensitive_validation(self):
        # Keys matching available entries in lowercase should not raise
        self.collect.chang = {"Added": ["x"]}
        self.collect.validate_keys(file_name="test.yaml")
