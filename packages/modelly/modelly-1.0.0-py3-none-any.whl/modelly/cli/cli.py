import sys

import typer
from modelly_client.cli import deploy_discord  # type: ignore
from rich.console import Console

from .commands import custom_component, deploy, print_environment_info, reload

app = typer.Typer()
app.command("environment", help="Print Modelly environment information.")(
    print_environment_info
)
app.command(
    "deploy",
    help="Deploy a Modelly app to Spaces. Must be called within the directory you would like to deploy.",
)(deploy)
app.command("deploy-discord", help="Deploy a Modelly app to Discord.")(
    deploy_discord.main
)


def cli():
    args = sys.argv[1:]
    if len(args) == 0:
        raise ValueError("No file specified.")
    if args[0] in {"deploy", "environment", "deploy-discord"}:
        app()
    elif args[0] in {"cc", "component"}:
        sys.argv = sys.argv[1:]
        custom_component()
    elif args[0] in {"build", "dev", "create", "show", "publish", "install"}:
        try:
            error = f"modelly {args[0]} is not a valid command. Did you mean `modelly cc {args[0]}` or `modelly component {args[0]}`?."
            raise ValueError(error)
        except ValueError:
            console = Console()
            console.print_exception()
    else:
        typer.run(reload)
