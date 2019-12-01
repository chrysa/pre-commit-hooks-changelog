import argparse
import sys
from typing import Optional
from typing import Sequence

from changelog import Changelog
from formater import Formatter

CHANGELOG_ENTRY_AVAILABLE = [
    "added",
    "modified",
    "removed",
    "upgraded",
    "unreleased",
    "blocked",
    "todo",
]


def main(argv: Optional[Sequence[str]] = None) -> int:
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
        "--changelog_folder",
        type=str,
        default="changelog",
        dest="changelog_folder",
        help="source folder of changelogs",
    )
    parser.add_argument(
        "--rebuild", action="store_true", help="rebuild changelog from scratch"
    )
    args = parser.parse_args(argv)
    process = Changelog(args=args, changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE)
    process.collect()
    formatter = Formatter(changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE)
    formatter.generate(
        archives_path=process.changelog_folder_archive_path,
        changelog_path=process.changelog_path,
        content_dict=process.changelog_content,
        rebuild=args.rebuild,
    )


if __name__ == "__main__":
    sys.exit(main())
