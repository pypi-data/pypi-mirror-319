from .const import svg_ignore_file
from .node.base import SvgManager
from .node import *
from .res import SvgResManager


def new_svg_manager(set_manager):
    return SvgManager(set_manager, SvgResManager(set_manager, [svg_ignore_file]))
