import argparse
import pathlib
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Dict
from typing import List

import ruamel.yaml

yaml = ruamel.yaml.YAML(typ="safe")


@dataclass(init=True)
class Changelog:
    args: argparse.Namespace
    chang: Dict[str, Dict] = field(default_factory=lambda: {})
    changelog_content: Dict[str, Dict] = field(default_factory=lambda: {})
    project_path: pathlib.PosixPath = Path().absolute()
    changelog_entry_available: List[str] = field(default_factory=lambda: [])

    @property
    def changelog_folder_path(self) -> pathlib.PosixPath:
        path = self.project_path / self.args.changelog_folder
        if not path.exists():
            raise NotADirectoryError(f"{path}")
        return path

    @property
    def changelog_folder_archive_path(self) -> pathlib.PosixPath:
        return self.changelog_folder_path / "archives"

    @property
    def changelog_path(self) -> pathlib.PosixPath:
        return self.project_path / self.args.output_file

    def collect(self) -> None:
        for file in self.changelog_folder_path.glob("*.yaml"):
            self.chang = yaml.load(file)
            self.validate_file(file_name=file.name)
            self.changelog_content[file.name.replace(".yaml", "")] = self.chang

    def validate_file(self, file_name) -> None:
        chang_keys = self.chang.keys()
        if not set([x.lower() for x in chang_keys]).issubset(
            self.changelog_entry_available
        ):
            for key in chang_keys:
                if key not in self.changelog_entry_available:
                    raise Exception(
                        f"key {key} in {file_name} not supported yet, only available {','.join(self.changelog_entry_available)}"
                    )
