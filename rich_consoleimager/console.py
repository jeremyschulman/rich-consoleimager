# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

import os
from typing import Optional
import asyncio
import xml.etree.ElementTree as ETree

# -----------------------------------------------------------------------------
# Public Imports
# -----------------------------------------------------------------------------

from tempfile import TemporaryDirectory
from rich.console import Console
from rich.terminal_theme import TerminalTheme, DEFAULT_TERMINAL_THEME
from html2image import Html2Image

# -----------------------------------------------------------------------------
# Exports
# -----------------------------------------------------------------------------

__all__ = ["ConsoleImage", "SVG_EXPORT_THEME"]

# -----------------------------------------------------------------------------
#
#                                 CODE BEGINS
#
# -----------------------------------------------------------------------------


# Use the default terminal in reverse as default SVG output theme.

SVG_EXPORT_THEME = DEFAULT_TERMINAL_THEME

SVG_EXPORT_THEME.foreground_color, SVG_EXPORT_THEME.background_color = (
    SVG_EXPORT_THEME.background_color,
    SVG_EXPORT_THEME.foreground_color,
)


class ConsoleImage:
    def __init__(
        self, console: Console, theme: Optional[TerminalTheme] = SVG_EXPORT_THEME
    ):
        self.console = console
        self.theme = theme
        self.tempdir: Optional[TemporaryDirectory] = None
        self.image_file: Optional[str] = None
        self._loop = asyncio.get_running_loop()

    async def render(self, title: str):
        """Creates the image file with the given title in the 'snapshot'"""
        svg_content = self.console.export_svg(title=title, theme=self.theme)

        # TODO: Warning!
        #       Extract the size of the image from the SVG file directly. This
        #       code is tightly bound to the output format of the SVG that Rich
        #       generates.  If Rich changes, this will break.  Going to see if
        #       there is a way to do this without hardcoding the XML path

        svg_xml = ETree.fromstring(svg_content)
        svg_rec_dict = svg_xml[1][0][0].attrib
        height = int(float(svg_rec_dict["height"]))
        width = int(float(svg_rec_dict["width"]))

        def create_png():
            """Creates the image.png file in the temp-directory"""
            self.tempdir = TemporaryDirectory()
            size = (width, height)
            _hti = Html2Image(output_path=self.tempdir.name, size=size)

            # if running as root (in docker for example), then do not use the
            # sandbox option.

            if os.geteuid() == 0:
                _hti.browser.flags = ["--no-sandbox"]

            _out_files = _hti.screenshot(
                html_str=svg_content,
                save_as="image.png",
            )
            self.image_file = _out_files[0]

        await self._loop.run_in_executor(None, create_png)

    async def cleanup(self):
        await self._loop.run_in_executor(None, self.tempdir.cleanup)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cleanup()
