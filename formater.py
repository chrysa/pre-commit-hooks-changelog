from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import List

from helper.markdown import Helper


@dataclass
class Formatter:
    level: int = 0
    content: str = None
    changelog_entry_available: List[str] = field(default_factory=lambda: [])

    @property
    def helper(self):
        return Helper(changelog_entry_available=self.changelog_entry_available)

    def generate(self, archives_path, changelog_path, content_dict):
        archives_path.mkdir(parents=True, exist_ok=True)
        latest_version = list(content_dict.keys())[-1]
        for version, content in content_dict.items():
            self.helper.title(value=version)
            self.content = self.helper.gen_content(content=content_dict[version])
            self.save(changelog_path=f"{archives_path / version}.md")
            self.helper.reset()

        self.helper.title(value=latest_version)
        self.content = self.helper.gen_content(content=content_dict[latest_version])
        self.content += self.helper.title(value="History", ret=True)
        self.content += self.generate_history(archives_path=archives_path, latest_version=latest_version)
        self.save(changelog_path=changelog_path)

    def generate_history(self, archives_path, latest_version):
        links = []
        for file in archives_path.glob('*.md'):
            version = file.name.replace('.md', '')
            if version != latest_version:
                links.append(self.helper.internal_link(target=file.relative_to(Path.cwd()), display=version))
        return self.helper.add_unordred_list(value=links, ret=True)

    def save(self, changelog_path, content=None):
        changelog_path = Path(changelog_path)
        with open(changelog_path, 'w+', encoding='UTF-8') as file:
            if content is None:
                file.write(self.content)
            else:
                file.write(content)
        if changelog_path.exists():
            print(f"{changelog_path} [\033[92mCREATED\33[37m]")
        else:
            print(f"{changelog_path} [\033[91mFAILED\33[37m]")
