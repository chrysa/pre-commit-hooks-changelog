from typing import Dict, List, Union, Optional
from dataclasses import field, dataclass


@dataclass(init=True)
class Helper:
    changelog_entry_available: List[str] = field(default_factory=list)
    level: int = 1
    content: str = ""

    def title(self, value: str) -> str:
        self.level += 1
        return f"# {value.title()}\n\n"

    def add_header(
        self, value: str, level: int = None, empty_lines: int = 2
    ) -> Optional[str]:
        if level is not None:
            self.level = level
        content = f"{'#' * self.level} {value.title()}"
        for i in range(0, (empty_lines - 1)):
            content += "\n" * i
        self.level += 1
        self.content += content
        if level is not None:
            return content
        return None

    def add_line(self, value: str) -> None:
        self.content += f"{value}\n"

    def add_unordred_list(self, value: List[str]) -> str:
        content = "\n"
        for item in value:
            if isinstance(item, str):
                content += f"* {item}\n"
            else:
                raise Exception(f"type {type(item)} is not supported")
        return content

    def gen_content(
        self,
        content: Union[
            str, List[str], Dict[str, Dict[str, List[str]]], Dict[str, List[str]]
        ],
    ) -> str:
        if isinstance(content, str):
            if content in self.changelog_entry_available:
                self.add_header(value=content)
            else:
                self.add_line(value=content)
        elif isinstance(content, list):
            self.content += self.add_unordred_list(value=content)
        elif isinstance(content, dict):
            for key, value in content.items():
                if self.level > 6:
                    raise Exception(f"only 6 subtitle available but get {self.level}")
                elif key in self.changelog_entry_available:
                    self.level = 2
                    self.gen_content(content=key)
                    self.gen_content(content=value)
                else:
                    self.level += 1
                    self.gen_content(content=value)
        else:
            raise Exception(f"type {type(content)} is not supported")
        self.content += "\n"
        return self.content

    def internal_link(self, target: str, display: str) -> str:
        return f"[{display}]({target})"

    def reset(self) -> None:
        self.level = 1
        self.content = ""
