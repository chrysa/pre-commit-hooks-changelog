import pathlib

import pytest

from pre_commit_hook.formatter import Formatter

_CONTENT = {"1.0.0.yaml": {"Added": ["a feature"]}}


def _spy_steps(mocker):
    """Replace every side-effecting step so a test observes dispatch, not file IO."""
    return {
        name: mocker.patch.object(Formatter, name, autospec=True)
        for name in (
            "remove_home_changelog",
            "remove_archives",
            "remove_latest",
            "generate_latest",
            "generate_versions",
            "generate_home_changelog",
        )
    }


def _called(steps):
    return {name for name, spy in steps.items() if spy.called}


class TestGenerateDispatch:
    @pytest.mark.parametrize(
        ("rebuild", "expected"),
        [
            (
                "all",
                {
                    "remove_home_changelog",
                    "remove_archives",
                    "generate_versions",
                    "generate_home_changelog",
                },
            ),
            ("versions", {"remove_archives", "generate_versions"}),
            (
                "latest",
                {
                    "remove_latest",
                    "generate_latest",
                    "remove_home_changelog",
                    "generate_home_changelog",
                },
            ),
            ("home", {"remove_home_changelog", "generate_home_changelog"}),
            (None, {"generate_versions", "generate_home_changelog"}),
            ("unknown-mode", {"generate_versions", "generate_home_changelog"}),
        ],
    )
    def test_mode_runs_its_own_steps(self, rebuild, expected, tmp_path, mocker):
        # GIVEN every side-effecting step replaced by a spy
        steps = _spy_steps(mocker)

        # WHEN generating with this rebuild mode
        Formatter().generate(
            archives_path=tmp_path / "archives",
            changelog_path=tmp_path / "CHANGELOG.md",
            content_dict=_CONTENT,
            rebuild=rebuild,
        )

        # THEN exactly the steps of that mode ran
        assert _called(steps) == expected

    def test_unknown_mode_falls_back_to_default(self, tmp_path, mocker):
        # GIVEN spies on the steps of the default strategy
        steps = _spy_steps(mocker)

        # WHEN an unknown mode is requested
        Formatter().generate(
            archives_path=tmp_path / "archives",
            changelog_path=tmp_path / "CHANGELOG.md",
            content_dict=_CONTENT,
            rebuild="does-not-exist",
        )

        # THEN nothing is removed — an unknown mode must never destroy a changelog
        assert not steps["remove_home_changelog"].called
        assert not steps["remove_archives"].called


class TestGenerateIntegration:
    def test_default_mode_writes_home_and_archive(self, tmp_path):
        # GIVEN an empty tree and one version of content
        archives_path = tmp_path / "archives"
        changelog_path = tmp_path / "CHANGELOG.md"

        # WHEN generating with no rebuild mode
        Formatter(changelog_entry_available=["Added"]).generate(
            archives_path=archives_path,
            changelog_path=changelog_path,
            content_dict=_CONTENT,
            rebuild=None,
        )

        # THEN both the home changelog and the version archive exist
        assert changelog_path.exists()
        assert (archives_path / "1.0.0.md").exists()

    def test_home_mode_keeps_existing_archives(self, tmp_path):
        # GIVEN an archive already generated
        archives_path = tmp_path / "archives"
        changelog_path = tmp_path / "CHANGELOG.md"
        formatter = Formatter(changelog_entry_available=["Added"])
        formatter.generate(
            archives_path=archives_path,
            changelog_path=changelog_path,
            content_dict=_CONTENT,
            rebuild=None,
        )
        archive: pathlib.Path = archives_path / "1.0.0.md"
        assert archive.exists()

        # WHEN rebuilding only the home page
        formatter.generate(
            archives_path=archives_path,
            changelog_path=changelog_path,
            content_dict=_CONTENT,
            rebuild="home",
        )

        # THEN the archive survived
        assert archive.exists()
