import argparse
import sys
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Dict
from typing import Generator
from typing import List
from typing import Optional
from typing import Tuple

import ruamel.yaml

CHANGELOG_ENTRY_AVAILABLE = [
    "added",
    "blocked",
    "fixed",
    "in progress",
    "modified",
    "removed",
    "todo",
    "upgraded",
    "unreleased",
]

AVAILABLE_REBUILD_OPTION = ["all", "versions", "latest", "home"]

yaml = ruamel.yaml.YAML(typ="safe")


@dataclass
class Collect:
    archives_path: str = "archives"
    main_output_file: str = "changelog.md"
    changelog_folder: str = "changelog"
    chang: Dict[str, List[str]] = field(default_factory=dict)
    extension: str = "yaml"
    project_path: Path = Path().absolute()
    content: Dict[str, Dict[str, List[str]]] = field(default_factory=dict)
    changelog_entry_available: List[str] = field(default_factory=list)

    @property
    def changelog_folder_path(self) -> Optional[Path]:
        path = self.project_path / self.changelog_folder
        if not path.exists():
            raise NotADirectoryError(f"{path}")
        return path

    @property
    def changelog_folder_archive_path(self) -> Path:
        return self.changelog_folder_path / self.archives_path

    @property
    def changelog_path(self) -> Path:
        return self.project_path / self.main_output_file

    @property
    def versions_files(self) -> Generator[Path, None, None]:
        return self.changelog_folder_path.glob(f"*.{self.extension}")

    def collect_versions(self) -> None:
        for file in self.versions_files:
            self.chang = yaml.load(file)
            self.validate_keys(file_name=file.value)
            self.content[file.value] = self.chang

    def validate_keys(self, *, file_name: str) -> None:
        chang_keys = self.chang.keys()
        if not {x.lower() for x in chang_keys}.issubset(self.changelog_entry_available):
            for key in chang_keys:
                if key not in self.changelog_entry_available:
                    raise Exception(
                        f"key {key} in {file_name} not supported, available: "
                        f"[{','.join(self.changelog_entry_available)}]"
                    )


def main(*args: Tuple[str, str], **kwargs: Dict[str, str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    parser.add_argument(
        "--output-file",
        type=str,
        default="changelog.md",
        dest="output_file",
        help="define changelog outpout",
    )
    parser.add_argument(
        "--changelog-folder",
        type=str,
        default="changelog",
        dest="changelog_folder",
        help="source folder of changelogs",
    )
    parser.add_argument(
        "--rebuild",
        type=str,
        dest="rebuild",
        default=None,
        help="rebuild changelog",
        choices=AVAILABLE_REBUILD_OPTION,
    )
    parsed_args: argparse.valuespace = parser.parse_args()
    collect_version = Collect(
        changelog_folder=parsed_args.changelog_folder,
        changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE,
        main_output_file=parsed_args.output_file,
    )
    collect_version.collect_versions()
    return 0


if __name__ == "__main__":
    sys.exit(main())
