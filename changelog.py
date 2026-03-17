import pathlib
import argparse
from typing import Dict, List, Optional
from pathlib import Path
from dataclasses import field, dataclass

import ruamel.yaml

yaml = ruamel.yaml.YAML(typ="safe")


@dataclass(init=True)
class Changelog:
    args: argparse.Namespace
    chang: Dict[str, List[str]] = field(default_factory=dict)
    changelog_content: Dict[str, Dict[str, List[str]]] = field(default_factory=dict)
    project_path: pathlib.Path = Path().absolute()
    changelog_entry_available: List[str] = field(default_factory=list)

    @property
    def changelog_folder_path(self) -> Optional[pathlib.PosixPath]:
        path = self.project_path / self.args.changelog_folder
        if not path.exists():
            raise NotADirectoryError(f"{path}")
        return path

    @property
    def changelog_folder_archive_path(self) -> pathlib.Path:
        return self.changelog_folder_path / "archives"

    @property
    def changelog_path(self) -> pathlib.PosixPath:
        return self.project_path / self.args.output_file

    def collect(self) -> None:
        for file in self.changelog_folder_path.glob("*.yaml"):
            self.chang = yaml.load(file)
            self.validate_file(file_name=file.name)
            self.changelog_content[file.name] = self.chang

    def validate_file(self, file_name: str) -> None:
        chang_keys = self.chang.keys()
        if not set([x.lower() for x in chang_keys]).issubset(
            self.changelog_entry_available
        ):
            for key in chang_keys:
                if key not in self.changelog_entry_available:
                    raise Exception(
                        f"key {key} in {file_name} not supported, available: "
                        f"[{','.join(self.changelog_entry_available)}]"
                    )
