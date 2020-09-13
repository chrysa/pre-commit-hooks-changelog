import sys
import argparse
from typing import Optional, Sequence

from pre_commit_hook_old.formater import Formatter
from pre_commit_hook_old.changelog import Changelog

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
    )
    args = parser.parse_args(argv)
    if args.rebuild and args.rebuild not in AVAILABLE_REBUILD_OPTION:
        print(f"{args.rebuild} is not a valid option for rebuild")
        sys.exit()
    process = Changelog(args=args, changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE)
    process.collect()
    formatter = Formatter(changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE)
    formatter.generate(
        archives_path=process.changelog_folder_archive_path,
        changelog_path=process.changelog_path,
        content_dict=process.changelog_content,
        rebuild=args.rebuild,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
