# SPDX-License-Identifier: LGPL-3.0-only

"""Package for doorstop."""

from importlib.metadata import PackageNotFoundError, version

from doorstop.common import DoorstopError, DoorstopInfo, DoorstopWarning
from doorstop.core import (
    Document,
    Item,
    Tree,
    build,
    builder,
    editor,
    exporter,
    find_document,
    find_item,
    importer,
    publisher,
)

__project__ = "Doorstop"

try:
    __version__ = version(__project__)
except PackageNotFoundError:
    __version__ = "(local)"

CLI = "doorstop"
GUI = "doorstop-gui"
SERVER = "doorstop-server"
VERSION = "{0} v{1}".format(__project__, __version__)
DESCRIPTION = "Requirements management using version control."
