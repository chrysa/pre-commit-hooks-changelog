import pytest
from pathlib import Path

from pre_commit_hook.generate_changelog import CHANGELOG_ENTRY_AVAILABLE


@pytest.fixture
def changelog_entry_available():
    return CHANGELOG_ENTRY_AVAILABLE


@pytest.fixture
def simple_yaml_content():
    return {"added": ["feature A", "feature B"], "fixed": ["bug X"]}


@pytest.fixture
def multi_version_content():
    return {
        "v1.0.0.yaml": {"added": ["initial release"]},
        "v1.1.0.yaml": {"fixed": ["bug fix"], "added": ["new feature"]},
        "v1.2.0.yaml": {"upgraded": ["dependency update"]},
    }


@pytest.fixture
def changelog_dir(tmp_path):
    folder = tmp_path / "changelog"
    folder.mkdir()
    return folder


@pytest.fixture
def populated_changelog_dir(tmp_path):
    folder = tmp_path / "changelog"
    folder.mkdir()
    (folder / "v1.0.0.yaml").write_text("added:\n  - initial release\n")
    (folder / "v1.1.0.yaml").write_text("fixed:\n  - bug fix\nadded:\n  - new feature\n")
    (folder / "v1.2.0.yaml").write_text("upgraded:\n  - dependency update\n")
    return tmp_path
