from dataclasses import dataclass
from dataclasses import field
from typing import Dict
from typing import List
from typing import Optional
from typing import Union


@dataclass
class Helper:
    changelog_entry_available: List[str] = field(default_factory=list)
    level: int = 1
    content: str = ""

    def title(self, value: str) -> str:
        self.level += 1
        return f"# {value.title()}\n\n"

    def add_header(self, value: str, level: int = None, empty_lines: int = 2) -> Optional[str]:
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

    @staticmethod
    def add_unordered_list(value: List[str]) -> str:
        content = "\n"
        for item in value:
            if isinstance(item, str):
                content += f"* {item}\n"
            else:
                raise TypeError(f"type {type(item)} is not supported in unordered list")
        return content

    def gen_content(
        self,
        content: Union[str, List[str], Dict[str, Dict[str, List[str]]], Dict[str, List[str]]],
    ) -> str:
        if isinstance(content, str):
            if content in self.changelog_entry_available:
                self.add_header(value=content)
            else:
                self.add_line(value=content)
        elif isinstance(content, list):
            self.content += self.add_unordered_list(value=content)
        elif isinstance(content, dict):
            for key, value in content.items():
                if self.level > 6:
                    raise ValueError(f"only 6 header levels available, got level {self.level}")
                elif key in self.changelog_entry_available:
                    self.level = 2
                    self.gen_content(content=key)
                    self.gen_content(content=value)
                else:
                    self.level += 1
                    self.gen_content(content=value)
        else:
            raise TypeError(f"type {type(content)} is not supported")
        self.content += "\n"
        return self.content

    @staticmethod
    def internal_link(target: str, display: str) -> str:
        return f"[{display}]({target})"

    def reset(self) -> None:
        self.level = 1
        self.content = ""
