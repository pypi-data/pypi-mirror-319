from typing import Optional

import typer
from typing_extensions import Annotated

from oracle import __version__
from oracle.controller import Controller
from oracle.display import Display
from oracle.model.group import ChoiceGroup

app = typer.Typer()
display = Display()
controller = Controller(display=display)


@app.callback(invoke_without_command=True, no_args_is_help=True)
def main(
    ctx: typer.Context,
    version: Annotated[
        Optional[bool], typer.Option("--version", help="Show version information")
    ] = False,
) -> None:
    """A pairwise comparer to discover your truth"""
    if version:
        display.diagnostic(f"{__package__} {__version__}")

    if ctx.invoked_subcommand is None:
        pass


@app.command()
def trial() -> None:
    """Perform a trial for the current choices"""
    display.success("oracle is determining your fate")
    with controller:
        options = controller.generate_trial()
        if not options:
            raise typer.Exit()

        # TODO(mmoran): what if the user types in the option instead of the number
        choice = typer.prompt("[>] 0 or 1?", type=int)

        for i, option in enumerate(options):
            if i == choice:
                option.success()
            else:
                option.trial()


@app.command()
def fate(
    verbose: Annotated[
        int,
        typer.Option(
            "--verbose",
            "-v",
            envvar="VERBOSE",
            show_envvar=True,
            count=True,
            help="Display additional diagnostics",
        ),
    ] = 0,
    final: Annotated[
        bool, typer.Option("--final", help="Clear all data after the result is generated")
    ] = False,
) -> None:
    """Reveal the fate of the current choices"""
    with controller:
        controller.generate_result(verbose=verbose)

        if final:
            display.warning("oracle has spoken")
            controller.group.reset()
        # TODO(mmoran): should oracle record the result as a trial?


@app.command()
def show(
    verbose: Annotated[
        int,
        typer.Option(
            "--verbose",
            "-v",
            envvar="VERBOSE",
            show_envvar=True,
            count=True,
            help="Display additional diagnostics",
        ),
    ] = 0
) -> None:
    """Show the available choices"""
    with controller:
        for choice in controller.group.choices:
            details = f" ({choice.successes}/{choice.trials})" if verbose else ""
            message = f"{choice.name}{details}"
            display.info(message)


@app.command()
def add(name: str) -> None:
    """Add a new choice to the available choices"""
    with controller:
        controller.update_choices(add=name)


@app.command()
def remove(name: str) -> None:
    """Remove a choice from the available choices"""
    with controller:
        controller.update_choices(remove=name)


@app.command()
def reset() -> None:
    """Reset the active choices to have no saved trials"""
    controller.refresh()
    controller.group.reset()
    controller.save()
    display.success("oracle has reset your choices")


@app.command()
def clear() -> None:
    """Clear all saved information"""
    controller.refresh()
    controller.group = ChoiceGroup()
    controller.save()
    display.success("oracle has forgotten everything")


if __name__ == "__main__":
    app()
