from typing import Dict, List, Optional
from dataclasses import field, dataclass


@dataclass
class Helper:
    changelog_entry_available: List[str] = field(default_factory=list)
    level: int = 1
    content: str = ""

    def title(self, value: str, ret: bool = False) -> str:
        data = self.add_header(value=value, ret=ret)
        self.level += 1
        return data

    def add_header(self, value: str, ret: bool = False) -> Optional[str]:
        data = f"{'#' * self.level} {value}\n"
        if ret:
            return data
        else:
            self.content += data

    def add_line(self, value: str) -> None:
        self.content += f"{value}\n"

    def add_unordred_list(self, value: List, ret: bool = False) -> Optional[str]:
        content = ""
        for item in value:
            if isinstance(item, str):
                content += f"* {item}\n"
            else:
                raise Exception(f"type {type(item)} is not supported")
        if ret:
            return content
        else:
            self.content += content

    def gen_content(self, content: Dict) -> str:
        if isinstance(content, str):
            if content in self.changelog_entry_available:
                self.add_header(value=content)
            else:
                self.add_line(value=content)
        elif isinstance(content, list):
            self.add_unordred_list(value=content)
        elif isinstance(content, dict):
            for key, value in content.items():
                if key in self.changelog_entry_available:
                    self.level = 2
                else:
                    self.level += 1
                if self.level > 6:
                    raise Exception(f"only 6 subtitle available but get {self.level}")
                self.add_header(value=key)
                self.gen_content(content=value)
        else:
            raise Exception(f"type {type(content)} is not supported")
        return self.content

    def internal_link(self, target: str, display: str) -> str:
        return f"[{display}]({target})"

    def reset(self) -> None:
        self.level = 1
        self.content = ""
