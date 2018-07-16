"""
Entry point when installing via pip
"""
from CLSearch.command import Run


def launch():
    """
    Launch script.
    """
    Run().cmdloop()


if __name__ == '__main__':
    launch()
