import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from pre_commit_hook.generate_changelog import main


class TestMain:
    def test_returns_zero_when_no_content(self, tmp_path, mocker):
        # GIVEN a changelog folder that exists but contains no YAML files
        # WHEN main() is called
        # THEN it returns 0 (success, nothing to generate)
        changelog_folder = tmp_path / "changelog"
        changelog_folder.mkdir()
        mocker.patch("sys.argv", ["generate-changelog"])
        mocker.patch.object(Path, "absolute", return_value=tmp_path)
        result = main()
        assert result == 0

    def test_returns_one_on_missing_changelog_folder(self, tmp_path, mocker):
        # GIVEN a project_path with no changelog subfolder
        # WHEN main() is called
        # THEN it returns 1 (NotADirectoryError is caught and converted to exit code 1)
        mocker.patch("sys.argv", ["generate-changelog"])
        mocker.patch.object(Path, "absolute", return_value=tmp_path)
        result = main()
        assert result == 1

    def test_returns_one_on_invalid_yaml_key(self, tmp_path, mocker):
        # GIVEN a YAML file with an unsupported section key
        # WHEN main() is called
        # THEN it returns 1 (ValueError is caught and converted to exit code 1)
        changelog_folder = tmp_path / "changelog"
        changelog_folder.mkdir()
        (changelog_folder / "v1.0.0.yaml").write_text("invalid_key:\n  - entry\n")
        mocker.patch("sys.argv", ["generate-changelog"])
        mocker.patch.object(Path, "absolute", return_value=tmp_path)
        result = main()
        assert result == 1

    def test_returns_zero_on_successful_generation(self, tmp_path, mocker):
        # GIVEN a valid YAML changelog file
        # WHEN main() is called
        # THEN it returns 0 and the changelog.md is created
        changelog_folder = tmp_path / "changelog"
        changelog_folder.mkdir()
        (changelog_folder / "v1.0.0.yaml").write_text("added:\n  - initial release\n")
        mocker.patch("sys.argv", ["generate-changelog"])
        mocker.patch.object(Path, "absolute", return_value=tmp_path)
        result = main()
        assert result == 0
        assert (tmp_path / "changelog.md").exists()
