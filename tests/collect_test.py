from pre_commit_hook import Collect


class TestCollect:
    class TestDefault:
        def test_path_generation(self, tmp_path, mocker):
            # GIVEN generate changelog path with default changelog path
            # WHEN initialise Collect object
            # THEN set property on Collect object
            changelog_folder = tmp_path / "changelog"
            changelog_folder.mkdir()
            collect = Collect()
            mocker.patch.object(collect, "project_path")
            collect.project_path = tmp_path
            assert collect.changelog_folder_path == changelog_folder, "project_path is not set correctly"

        def test_changelog_path_path_generation(self, tmp_path, mocker):
            # GIVEN generate changelog path with default main_output_file
            # WHEN initialise Collect object
            # THEN set property on Collect object
            output_file = tmp_path / "changelog.md"
            collect = Collect()
            mocker.patch.object(collect, "project_path")
            collect.project_path = tmp_path
            assert collect.changelog_path == output_file

    # test raise
    class TestCustom:
        def test_path_generation(self, tmp_path, mocker):
            # GIVEN generate changelog path with custom changelog path
            # WHEN initialise Collect object
            # THEN set property on Collect object
            changelog_folder = tmp_path / "changelog_path"
            changelog_folder.mkdir()
            collect = Collect(changelog_folder="changelog_path")
            mocker.patch.object(collect, "project_path")
            collect.project_path = tmp_path
            assert collect.changelog_folder_path == changelog_folder, "custom project_path is not set correctly"
