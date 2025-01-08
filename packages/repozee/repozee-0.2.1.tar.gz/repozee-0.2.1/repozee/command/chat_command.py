from pathlib import Path
from wizlib.parser import WizParser

from repozee.ai import AI
from repozee.command import RepoZeeCommand
from repozee.toolset import Toolset


class ChatCommand(RepoZeeCommand):

    name = 'chat'

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        parser.add_argument('directory', default="", nargs='?')

    def handle_vals(self):
        super().handle_vals()
        if not self.provided('directory'):
            self.directory = str(Path.cwd())

    @RepoZeeCommand.wrap
    def execute(self):
        toolset = Toolset(self.directory)
        repozee = AI(toolset)
        repozee.chat()
