import click

from . import legacy

__all__ = ["main"]


@click.group(name="BASE_dzne")
def main():
    pass


main.add_command(legacy.main, name="legacy")
