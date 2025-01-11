import importlib.resources

import tomli


def getconfig():
    with (
        importlib.resources.files("BASE_dzne.core.legacy.libBASE")
        .joinpath("config.toml")
        .open("rb") as stream
    ):
        return tomli.load(stream)


def getprimer():
    with (
        importlib.resources.files("BASE_dzne.core.legacy.libBASE")
        .joinpath("primer.toml")
        .open("rb") as stream
    ):
        return tomli.load(stream)


CONFIG = getconfig()
PRIMER = getprimer()
