import unittest

import click

__all__ = ["main", "test"]

@class.command(name="test")
def main():
    test()

def test():
    loader = unittest.TestLoader()
    tests = loader.discover(start_dir="BASE_dzne.core.legacy.tests")
    runner = unittest.TextTestRunner()
    result = runner.run(tests)
    return result
