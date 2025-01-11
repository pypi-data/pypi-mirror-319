from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich import print

import modelly
from modelly.analytics import custom_component_analytics
from modelly.cli.commands.components.install_component import _get_executable_path

modelly_template_path = Path(modelly.__file__).parent / "templates" / "frontend"


def _dev(
    app: Annotated[
        Path,
        typer.Argument(
            help="The path to the app. By default, looks for demo/app.py in the current directory."
        ),
    ] = Path("demo") / "app.py",
    component_directory: Annotated[
        Path,
        typer.Option(
            help="The directory with the custom component source code. By default, uses the current directory."
        ),
    ] = Path("."),
    host: Annotated[
        str,
        typer.Option(
            help="The host to run the front end server on. Defaults to localhost.",
        ),
    ] = "localhost",
    python_path: Annotated[
        Optional[str],
        typer.Option(
            help="Path to python executable. If None, will use the default path found by `which python3`. If python3 is not found, `which python` will be tried. If both fail an error will be raised."
        ),
    ] = None,
    modelly_path: Annotated[
        Optional[str],
        typer.Option(
            help="Path to modelly executable. If None, will use the default path found by `shutil.which`."
        ),
    ] = None,
):
    custom_component_analytics(
        "dev",
        None,
        None,
        None,
        None,
        python_path=python_path,
        modelly_path=modelly_path,
    )
    component_directory = component_directory.resolve()

    print(f":recycle: [green]Launching[/] {app} in reload mode\n")

    node = shutil.which("node")
    if not node:
        raise ValueError("node must be installed in order to run dev mode.")

    python_path = _get_executable_path(
        "python", python_path, cli_arg_name="--python-path", check_3=True
    )
    modelly_path = _get_executable_path(
        "modelly", modelly_path, cli_arg_name="--modelly-path"
    )

    modelly_node_path = subprocess.run(
        [node, "-e", "console.log(require.resolve('@modelly/preview'))"],
        cwd=Path(component_directory / "frontend"),
        check=False,
        capture_output=True,
    )

    if modelly_node_path.returncode != 0:
        raise ValueError(
            "Could not find `@modelly/preview`. Run `npm i -D @modelly/preview` in your frontend folder."
        )

    modelly_node_path = modelly_node_path.stdout.decode("utf-8").strip()

    proc = subprocess.Popen(
        [
            node,
            modelly_node_path,
            "--component-directory",
            component_directory,
            "--root",
            modelly_template_path,
            "--app",
            str(app),
            "--mode",
            "dev",
            "--host",
            host,
            "--python-path",
            python_path,
            "--modelly-path",
            modelly_path,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    while True:
        proc.poll()
        text = proc.stdout.readline()  # type: ignore
        err = None
        if proc.stderr:
            err = proc.stderr.readline()

        text = (
            text.decode("utf-8")
            .replace("Changes detected in:", "[orange3]Changed detected in:[/]")
            .replace("Watching:", "[orange3]Watching:[/]")
            .replace("Running on local URL", "[orange3]Backend Server[/]")
        )

        if "[orange3]Watching:[/]" in text:
            text += f"'{str(component_directory / 'frontend').strip()}',"
        if "To create a public link" in text:
            continue
        print(text)
        if err:
            print(err.decode("utf-8"))

        if proc.returncode is not None:
            print("Backend server failed to launch. Exiting.")
            return
