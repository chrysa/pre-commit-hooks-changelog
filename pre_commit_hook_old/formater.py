import pathlib
from typing import Dict, List, Union
from pathlib import Path
from dataclasses import field, dataclass

from .helper.markdown import Helper


@dataclass
class Formatter:
    level: int = 0
    content: str = None
    changelog_entry_available: List[str] = field(default_factory=list)

    @property
    def helper(self) -> Helper:
        return Helper(changelog_entry_available=self.changelog_entry_available)

    def generate(
        self,
        archives_path: pathlib.Path,
        changelog_path: pathlib.Path,
        content_dict: Dict[str, Dict[str, List[str]]],
        rebuild: str = "",
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
            content_dict=content_dict,
            version=latest_version,
        )

    def generate_version(
        self,
        archives_path: pathlib.Path,
        content_dict: Union[Dict[str, Dict[str, List[str]]], Dict[str, List[str]]],
        version: str,
    ) -> None:
        self.content = self.helper.title(value=version.replace(".yaml", ""))
        self.content += self.helper.gen_content(content=content_dict)
        self.save(
            changelog_path=archives_path / version,
            archives_path=archives_path,
        )

    @staticmethod
    def remove_version(archives_path: pathlib.Path, version: str) -> None:
        file = archives_path / version
        if file.exists():
            file.unlink()

    def generate_versions(
        self,
        archives_path: pathlib.Path,
        content_dict: Dict[str, Dict[str, List[str]]],
    ) -> None:
        for version, content in content_dict.items():
            self.content = self.helper.title(value=version.replace(".yaml", ""))
            self.content += self.helper.gen_content(content=content_dict)
            self.save(
                changelog_path=archives_path / version,
                archives_path=archives_path,
            )

    def generate_home_changelog(
        self,
        archives_path: pathlib.Path,
        changelog_path: pathlib.Path,
        content_dict: Dict[str, Dict[str, List[str]]],
    ) -> None:
        # generate front page
        latest_version = list(content_dict.keys())[-1]
        self.content = self.helper.title(value=latest_version.replace(".yaml", ""))
        self.content += self.helper.gen_content(content=content_dict[latest_version])
        if len(content_dict.keys()) > 1:
            self.remove_trailling_line(keep=2)
            self.content += self.helper.add_header(value="History", level=2, empty_lines=3)
            self.content += self.generate_history(
                archives_path=archives_path,
                latest_version=latest_version.replace(".yaml", ""),
            )
        self.save(
            changelog_path=changelog_path,
            archives_path=archives_path,
        )

    def generate_history(
        self,
        archives_path: pathlib.Path,
        latest_version: str,
    ) -> str:
        links = []
        for file in archives_path.glob("*.md"):
            version = file.name.replace(".md", "")
            if version != latest_version:
                links.append(self.helper.internal_link(target=file.relative_to(Path.cwd()).as_posix(), display=version))
        links.reverse()
        return self.helper.add_unordred_list(value=links)

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
        skip = False
        if changelog_path.exists():
            self.remove_trailling_line()
            with open(changelog_path.as_posix(), encoding="UTF-8") as file:
                if self.content == file.read():
                    skip = True
        return skip

    def remove_trailling_line(self, keep: int = 0) -> None:
        if self.content[-1] == "\n":
            self.content = self.content[:-1]
            self.remove_trailling_line()
        self.content += "\n" * keep

    def write_file(self, changelog_path: pathlib.Path, status: str) -> None:
        self.content += "\n"
        with open(changelog_path.as_posix(), "w+", encoding="UTF-8") as file:
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
        if not archives_path.exists() and not archives_path.is_dir():
            archives_path.mkdir(exist_ok=True)
        changelog_path = changelog_path.with_suffix(".md")
        if not changelog_path.exists():
            self.write_file(
                changelog_path=changelog_path,
                status="\033[92mCREATED\33[37m",
            )
        elif not self.compare_content(changelog_path=changelog_path):
            self.write_file(
                changelog_path=changelog_path,
                status="\33[33mUPDATED\33[37m",
            )
        else:
            print(f"{changelog_path} [\33[34mSKIPPED\33[37m]")
        self.helper.reset()
