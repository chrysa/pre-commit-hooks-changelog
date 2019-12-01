import filecmp
import pathlib
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Dict
from typing import List
from typing import Union

from helper.markdown import Helper, helper_T


@dataclass
class Formatter:
    level: int = 0
    content: str = None
    changelog_entry_available: List[str] = field(default_factory=lambda: [])

    @property
    def helper(self) -> helper_T:
        return Helper(changelog_entry_available=self.changelog_entry_available)

    def generate(
        self,
        archives_path: pathlib.PosixPath,
        changelog_path: pathlib.PosixPath,
        content_dict: Dict,
        rebuild: bool = False,
    ) -> None:
        if rebuild:
            self.remove(changelog_path=changelog_path, archives_path=archives_path)
        latest_version = list(content_dict.keys())[-1]
        # generate all versions
        for version, content in content_dict.items():
            self.content = self.helper.title(value=version, ret=True)
            self.content += self.helper.gen_content(content=content_dict[version])
            self.save(
                changelog_path=f"{archives_path / version}.md",
                archives_path=archives_path,
            )
            self.helper.reset()
        # generate front page
        self.content = self.helper.title(value=latest_version, ret=True)
        self.content += self.helper.gen_content(content=content_dict[latest_version])
        if len(content_dict.keys()) > 1:
            self.content += self.helper.title(value="History", ret=True)
            self.content += self.generate_history(
                archives_path=archives_path, latest_version=latest_version
            )
        self.save(changelog_path=changelog_path, archives_path=archives_path)

    def generate_history(
        self, archives_path: pathlib.PosixPath, latest_version: str
    ) -> Union[str, None]:
        links = []
        for file in archives_path.glob("*.md"):
            version = file.name.replace(".md", "")
            if version != latest_version:
                links.append(
                    self.helper.internal_link(
                        target=file.relative_to(Path.cwd()), display=version
                    )
                )
        return self.helper.add_unordred_list(value=links, ret=True)

    def remove(
        self, changelog_path: pathlib.PosixPath, archives_path: pathlib.PosixPath
    ) -> None:
        if changelog_path.exists():
            changelog_path.unlink()

        if archives_path.exists():
            if archives_path.is_dir():
                for file in archives_path.glob("*"):
                    if file.exists():
                        file.unlink()
                archives_path.rmdir()

    def save(
        self, changelog_path: pathlib.PosixPath, archives_path: pathlib.PosixPath
    ) -> None:
        changelog_path = Path(changelog_path)
        skip = False
        if changelog_path.exists():
            tmp = Path().absolute() / "tmp"
            with open(tmp.as_posix(), "w+", encoding="UTF-8") as file:
                file.write(self.content)
                if filecmp.cmp(changelog_path, tmp.as_posix()):
                    skip = True
                else:
                    changelog_path.unlink()
            if tmp.exists():
                tmp.unlink()
        if not archives_path.exists():
            if not archives_path.is_dir():
                archives_path.mkdir(exist_ok=True)
        if not skip:
            with open(changelog_path, "w+", encoding="UTF-8") as file:
                file.write(self.content)
            if changelog_path.exists():
                print(f"{changelog_path} [\033[92mCREATED\33[37m]")
            else:
                print(f"{changelog_path} [\033[91mFAILED\33[37m]")
