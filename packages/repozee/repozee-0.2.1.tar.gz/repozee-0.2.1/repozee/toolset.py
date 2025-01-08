
from pathlib import Path
from gitignore_parser import parse_gitignore
import subprocess
from typing import Optional, Dict, Any
import yaml

from repozee import load_definition


class Toolset:

    definitions = yaml.safe_load(load_definition('tools.yml'))

    def __init__(self, directory):
        self.directory = Path(directory)

    def list(self) -> list[str]:
        result = []
        gitignore = None
        gitignore_file = self.directory / '.gitignore'
        if gitignore_file.exists():
            gitignore = parse_gitignore(gitignore_file)
        for file_path in self.directory.rglob('*'):
            if '.git' in file_path.parts:
                continue
            if gitignore and gitignore(str(file_path)):
                continue
            result.append(str(file_path.relative_to(self.directory)))
        return result

    def read_file(self, file_path: str) -> str:
        path = self.directory / file_path
        return path.read_text()

    def git_diff(self, path: Optional[str] = None) -> str:
        cmd = ['git', 'diff', 'HEAD']

        if path is not None:
            full_path = self.directory / path
            if not full_path.exists():
                raise FileNotFoundError(f"Path does not exist: {path}")
            cmd.append(str(full_path.relative_to(self.directory)))

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                cwd=str(self.directory)
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            # Re-raise to allow caller to handle git errors
            raise
