from typing import Optional
import os

from rich.table import Table
from rich.console import Console
from rich.terminal_theme import TerminalTheme

from .console import ConsoleImage, SVG_EXPORT_THEME


class TableImage(ConsoleImage):
    """
    TableImage will take a Rich Table object and perfectly size fit it into an
    image file.  TableImage subclasses ConsoleImage.  As a Developer the usage
    as a context manager is the same.
    """

    def __init__(self, table: Table, theme: Optional[TerminalTheme] = SVG_EXPORT_THEME):
        """
        Construct a new TableImage instance from the given Rich.Table instance
        without having to first run it through a Console.  This constructor
        will create a temporary Console instance for the size-fitting purpose.

        Parameters
        ----------
        table: Table
            The source table instance that will be generated into an image.

        theme: TerminalTheme, optional
            This instance deteremines the terminal colors used when generating
            the SVG -> image file.  By default, the theme is the default
            terminal theme with reveresed fg / bg. That is white on black.
        """
        console = Console(file=open(os.devnull, "w"))
        console.print(table)
        table_sz = console.measure(table)
        console.width = table_sz.maximum
        console.record = True
        console.print(table)
        super().__init__(console=console, theme=theme)
