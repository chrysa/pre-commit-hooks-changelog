from dataclasses import dataclass
from dataclasses import field
from typing import List


@dataclass
class Helper:
    changelog_entry_available: List = field(default_factory=lambda: [])
    level: int = 1
    content: str = ''

    def title(self, value, ret=False):
        return self.add_header(value=value, ret=ret)
        self.level += 1

    def add_header(self, value, ret = False):
        data = f"{'#' * self.level} {value}\n"
        if ret:
            return data
        else:
           self.content += data

    def add_line(self, value):
        self.content += f"{value} \n"

    def add_unordred_list(self, value, ret = False):
        content = ''
        for item in value:
            if isinstance(item, str):
                content += f"* {item} \n"
            else:
                raise Exception(f"type {type(item)} is not supported")
        if ret:
            return content
        else:
            self.content += content

    def gen_content(self, content):
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

    def internal_link(self, target, display):
        return f"[{display}]({target})"

    def reset(self):
        self.level = 1
        self.content = ''