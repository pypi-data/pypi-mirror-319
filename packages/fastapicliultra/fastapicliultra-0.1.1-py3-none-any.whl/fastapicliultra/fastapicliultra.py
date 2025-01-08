import click

import init

@click.group()
def cli() -> None:
    """Command line interface for FastAPI Ultra."""
    pass


cli.add_command(init.init)
