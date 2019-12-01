import argparse
import collections
import io
import pathlib
import sys
from dataclasses import dataclass
from dataclasses import field
from pprint import pprint
from typing import Any, Generator, Optional, Sequence
from typing import DefaultDict
from typing import Dict

import ruamel.yaml
from pathlib import Path
from mdutils import MdUtils

CHANGELOG_ENTRY_AVAILABLE = ["added", "modified", "removed", "upgraded"]

yaml = ruamel.yaml.YAML(typ='safe')


class Markdown(object):
    @classmethod
    def generate(cls,file_path, content):
        # https://github.com/didix21/mdutils
        # gen for each old
            # add on content table
        # generate general
        markdown_content = MdUtils(file_name=file_path.as_posix(),
                                   title=list(content.keys())[
                                       -1].split('.')[0])
        markdown_content.create_md_file()


@dataclass(init=True)
class Changelog:
    chang: Dict[str, Dict] = field(default_factory=lambda: {})
    changelog_content: Dict[str, Dict] = field(default_factory=lambda: {})
    args: argparse.Namespace = None
    project_path: pathlib.PosixPath = Path().absolute()

    @property
    def changelog_folder_path(self) -> None:
        return self.project_path / self.args.changelog_folder

    @property
    def changelog_folder_archive_path(self) -> None:
        return self.changelog_folder_path / "archives"

    def remove(self) -> None:
        changelog_path = self.project_path / self.args.output_file
        if not Path.exists(changelog_path):
            raise FileNotFoundError(f"no {self.args.output_file} file found found, expected {changelog_path}")
        changelog_path.unlink()
        if self.changelog_folder_archive_path.is_dir():
            for file in self.changelog_folder_path.glob('*'):
                Path(file).unlink()
            self.changelog_folder_archive_path.rmdir()

    def build(self) -> None:
        for file in self.changelog_folder_path.glob('*.yaml'):
            self.chang = yaml.load(file)
            self.validate_file(file_name=file.name)
            self.changelog_content[file.name] = self.chang
        self.convert()

    def validate_file(self, file_name) -> None:
        chang_keys = self.chang.keys()
        if not set([x.lower() for x in chang_keys]).issubset(CHANGELOG_ENTRY_AVAILABLE):
            for key in chang_keys:
                if key not in CHANGELOG_ENTRY_AVAILABLE:
                    raise Exception(f"key {key} in {file_name} not supported yet")

    def convert(self):
        if self.args.output_file.endswith('.md'):
            self.args.output_file = self.args.output_file[:-3]
        file_path = self.project_path / self.args.output_file
        Markdown.generate(file_path=file_path, content=self.changelog_content)



def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    # parser.add_argument('filenames', type=str, nargs='*', help='file to add')
    parser.add_argument('--rebuild', action='store_true', help="rebuild changelog from scratch")
    parser.add_argument('--no-archive', action='store_true', help="not archive archive formatted versions")
    parser.add_argument('--output-file', type=str, default="changelog.md", dest="output_file",
                        help="define changelog outpout")
    parser.add_argument('--changelog_folder', type=str, default="changelog", dest="changelog_folder",
                        help="define changelog outpout")
    args = parser.parse_args(argv)
    process = Changelog(args=args)
    if process.args.rebuild:
        process.remove()
    process.build()


if __name__ == '__main__':
    sys.exit(main())
