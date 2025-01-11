import click

from . import aBASE, cBASE

__all__ = ["main"]


@click.group(name="legacy")
def main():
    pass


main.add_command(aBASE.main, name="aBASE")
main.add_command(cBASE.main, name="cBASE")
