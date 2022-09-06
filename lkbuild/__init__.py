"""
LensKit build support helpers.
"""

__version__ = "0.2.0"

def lkbuild_main():
    "Main entry point to run lkbuild tasks."
    from invoke import Program, Collection
    from . import tasks
    prog = Program(namespace=Collection.from_module(tasks),
                   name="lkbuild", binary="lkbuild",
                   version=__version__)
    prog.run()
