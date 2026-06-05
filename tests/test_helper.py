import pytest

from pre_commit_hook.helper import Helper
from pre_commit_hook.generate_changelog import CHANGELOG_ENTRY_AVAILABLE


@pytest.fixture
def helper():
    return Helper(changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE)


class TestHelperTitle:
    def test_returns_h1_markdown(self):
        h = Helper()
        result = h.title("v1.0.0")
        assert result == "# V1.0.0\n\n"

    def test_title_capitalises_value(self):
        h = Helper()
        result = h.title("my project")
        assert "My Project" in result

    def test_title_increments_level(self):
        h = Helper()
        assert h.level == 1
        h.title("v1.0.0")
        assert h.level == 2

    def test_does_not_modify_content(self):
        h = Helper()
        h.title("v1.0.0")
        assert h.content == ""


class TestHelperAddUnorderedList:
    def test_single_item(self):
        result = Helper.add_unordered_list(["item1"])
        assert result == "\n* item1\n"

    def test_multiple_items(self):
        result = Helper.add_unordered_list(["item1", "item2", "item3"])
        assert "* item1\n" in result
        assert "* item2\n" in result
        assert "* item3\n" in result

    def test_empty_list_returns_newline(self):
        result = Helper.add_unordered_list([])
        assert result == "\n"

    def test_non_string_item_raises(self):
        with pytest.raises(TypeError):
            Helper.add_unordered_list(["valid", 42])


class TestHelperAddHeader:
    def test_returns_header_at_current_level(self):
        h = Helper()
        h.level = 2
        result = h.add_header(value="Added", level=2)
        assert result.startswith("## Added")

    def test_sets_level_when_provided(self):
        h = Helper()
        h.add_header(value="test", level=3)
        assert h.level == 4

    def test_returns_none_without_level(self):
        h = Helper()
        result = h.add_header(value="test")
        assert result is None

    def test_appends_to_content(self):
        h = Helper()
        h.level = 2
        h.add_header(value="Section")
        assert "## Section" in h.content


class TestHelperGenContent:
    def test_string_changelog_entry_adds_header(self, helper):
        helper.level = 2
        helper.gen_content("added")
        assert "## Added" in helper.content

    def test_string_non_entry_adds_line(self, helper):
        helper.level = 3
        helper.gen_content("some note")
        assert "some note" in helper.content

    def test_list_adds_unordered_list(self, helper):
        result = helper.gen_content(["a", "b"])
        assert "* a" in result
        assert "* b" in result

    def test_dict_with_changelog_entry(self, helper):
        result = helper.gen_content({"added": ["feature X", "feature Y"]})
        assert "## Added" in result
        assert "* feature X" in result
        assert "* feature Y" in result

    def test_dict_with_multiple_entries(self, helper):
        result = helper.gen_content({"added": ["new"], "fixed": ["bug"]})
        assert "## Added" in result
        assert "## Fixed" in result

    def test_dict_with_nested_subsection(self, helper):
        result = helper.gen_content({"added": {"section": ["entry 1"]}})
        assert "## Added" in result
        assert "* entry 1" in result

    def test_invalid_type_raises_type_error(self, helper):
        with pytest.raises(TypeError):
            helper.gen_content(42)

    def test_returns_accumulated_content(self, helper):
        result = helper.gen_content({"added": ["x"]})
        assert result == helper.content

    def test_always_appends_newline(self, helper):
        helper.gen_content(["item"])
        assert helper.content.endswith("\n")


class TestHelperReset:
    def test_reset_clears_content(self, helper):
        helper.gen_content({"added": ["x"]})
        assert helper.content != ""
        helper.reset()
        assert helper.content == ""

    def test_reset_restores_level(self, helper):
        helper.gen_content({"added": ["x"]})
        helper.reset()
        assert helper.level == 1


class TestHelperInternalLink:
    def test_creates_markdown_link(self):
        result = Helper.internal_link(target="path/to/file.md", display="v1.0.0")
        assert result == "[v1.0.0](path/to/file.md)"

    def test_link_with_special_chars(self):
        result = Helper.internal_link(target="dir/v1.0.0.md", display="v1.0.0")
        assert result == "[v1.0.0](dir/v1.0.0.md)"
