import pathlib
from dataclasses import dataclass
from dataclasses import field
from typing import Dict
from typing import List
from typing import Optional

from .helper import Helper


@dataclass
class Formatter:
    changelog_entry_available: List[str] = field(default_factory=list)
    content: str = ""

    def _new_helper(self) -> Helper:
        return Helper(changelog_entry_available=self.changelog_entry_available)

    def generate(
        self,
        archives_path: pathlib.Path,
        changelog_path: pathlib.Path,
        content_dict: Dict[str, Dict[str, List[str]]],
        rebuild: Optional[str] = None,
    ) -> None:
        if rebuild == "all":
            self.remove_home_changelog(changelog_path=changelog_path)
            self.remove_archives(archives_path=archives_path)
            self.generate_versions(content_dict=content_dict, archives_path=archives_path)
            self.generate_home_changelog(
                content_dict=content_dict,
                changelog_path=changelog_path,
                archives_path=archives_path,
            )
        elif rebuild == "versions":
            self.remove_archives(archives_path=archives_path)
            self.generate_versions(content_dict=content_dict, archives_path=archives_path)
        elif rebuild == "latest":
            self.remove_latest(content_dict=content_dict, archives_path=archives_path)
            self.generate_latest(content_dict=content_dict, archives_path=archives_path)
            self.remove_home_changelog(changelog_path=changelog_path)
            self.generate_home_changelog(
                content_dict=content_dict,
                changelog_path=changelog_path,
                archives_path=archives_path,
            )
        elif rebuild == "home":
            self.remove_home_changelog(changelog_path=changelog_path)
            self.generate_home_changelog(
                content_dict=content_dict,
                changelog_path=changelog_path,
                archives_path=archives_path,
            )
        else:
            self.generate_versions(content_dict=content_dict, archives_path=archives_path)
            self.generate_home_changelog(
                content_dict=content_dict,
                changelog_path=changelog_path,
                archives_path=archives_path,
            )

    def remove_latest(
        self,
        archives_path: pathlib.Path,
        content_dict: Dict[str, Dict[str, List[str]]],
    ) -> None:
        latest_version = list(content_dict.keys())[-1]
        self.remove_version(archives_path=archives_path, version=latest_version)

    def generate_latest(
        self,
        archives_path: pathlib.Path,
        content_dict: Dict[str, Dict[str, List[str]]],
    ) -> None:
        latest_version = list(content_dict.keys())[-1]
        self.generate_version(
            archives_path=archives_path,
            version=latest_version,
            version_data=content_dict[latest_version],
        )

    def generate_version(
        self,
        archives_path: pathlib.Path,
        version: str,
        version_data: Dict[str, List[str]],
    ) -> None:
        helper = self._new_helper()
        version_title = version.replace(".yaml", "").replace(".yml", "")
        self.content = helper.title(value=version_title)
        self.content += helper.gen_content(content=version_data)
        self.save(changelog_path=archives_path / version, archives_path=archives_path)

    @staticmethod
    def remove_version(archives_path: pathlib.Path, version: str) -> None:
        file = (archives_path / version).with_suffix(".md")
        if file.exists():
            file.unlink()

    def generate_versions(
        self,
        archives_path: pathlib.Path,
        content_dict: Dict[str, Dict[str, List[str]]],
    ) -> None:
        for version, version_data in content_dict.items():
            self.generate_version(
                archives_path=archives_path,
                version=version,
                version_data=version_data,
            )

    def generate_home_changelog(
        self,
        archives_path: pathlib.Path,
        changelog_path: pathlib.Path,
        content_dict: Dict[str, Dict[str, List[str]]],
    ) -> None:
        latest_version = list(content_dict.keys())[-1]
        latest_version_title = latest_version.replace(".yaml", "").replace(".yml", "")
        helper = self._new_helper()
        self.content = helper.title(value=latest_version_title)
        self.content += helper.gen_content(content=content_dict[latest_version])
        if len(content_dict) > 1:
            history = self.generate_history(
                archives_path=archives_path,
                latest_version=latest_version_title,
            )
            if history:
                self._remove_trailing_newlines(keep=2)
                history_helper = self._new_helper()
                self.content += history_helper.add_header(value="History", level=2, empty_lines=3)
                self.content += history
        self.save(changelog_path=changelog_path, archives_path=archives_path)

    def generate_history(
        self,
        archives_path: pathlib.Path,
        latest_version: str,
    ) -> str:
        if not archives_path.exists():
            return ""
        helper = self._new_helper()
        links = []
        for file in sorted(archives_path.glob("*.md"), reverse=True):
            version = file.stem
            if version != latest_version:
                links.append(
                    helper.internal_link(
                        target=file.relative_to(archives_path.parent).as_posix(),
                        display=version,
                    )
                )
        if not links:
            return ""
        return helper.add_unordered_list(value=links)

    @staticmethod
    def remove_home_changelog(changelog_path: pathlib.Path) -> None:
        if changelog_path.exists():
            changelog_path.unlink()
            print(f"{changelog_path.as_posix()} [\33[33mREMOVED\33[37m]")

    @staticmethod
    def remove_archives(archives_path: pathlib.Path) -> None:
        if archives_path.exists() and archives_path.is_dir():
            for file in archives_path.glob("*"):
                if file.exists():
                    file.unlink()
                    print(f"{file.as_posix()} [\33[33mREMOVED\33[37m]")
            archives_path.rmdir()
            print(f"{archives_path.as_posix()} [\33[33mREMOVED\33[37m]")

    def compare_content(self, changelog_path: pathlib.Path) -> bool:
        if changelog_path.exists():
            with open(changelog_path, encoding="UTF-8") as file:
                file_content = file.read().rstrip("\n")
            return self.content.rstrip("\n") == file_content
        return False

    def _remove_trailing_newlines(self, keep: int = 0) -> None:
        self.content = self.content.rstrip("\n") + "\n" * keep

    def write_file(self, changelog_path: pathlib.Path, status: str) -> None:
        self.content += "\n"
        with open(changelog_path, "w", encoding="UTF-8") as file:
            file.write(self.content)
        if changelog_path.exists():
            print(f"{changelog_path.as_posix()} [{status}]")
        else:
            print(f"{changelog_path.as_posix()} [\033[91mFAILED\33[37m]")

    def save(
        self,
        changelog_path: pathlib.Path,
        archives_path: pathlib.Path,
    ) -> None:
        archives_path.mkdir(parents=True, exist_ok=True)
        changelog_path = changelog_path.with_suffix(".md")
        if not changelog_path.exists():
            self.write_file(changelog_path=changelog_path, status="\033[92mCREATED\33[37m")
        elif not self.compare_content(changelog_path=changelog_path):
            self.write_file(changelog_path=changelog_path, status="\33[33mUPDATED\33[37m")
        else:
            print(f"{changelog_path} [\33[34mSKIPPED\33[37m]")
