import typer
from pyopenbot.commands.run import Run
from pyopenbot.commands.init import Init
from pyopenbot.commands.check import Check
from pyopenbot.platforms.cli_platform import CLIPlatform

class CLI:
    def __init__(self):
        self.app: typer.Typer = typer.Typer(
            help="OpenBot CLI", no_args_is_help=True
        )

        self.platform = CLIPlatform()

        self.app.command("run")(Run(self.platform).run)
        self.app.command("init")(Init(self.platform).run)
        self.app.command("check")(Check(self.platform).run)

    def run(self) -> None:
        self.app()
