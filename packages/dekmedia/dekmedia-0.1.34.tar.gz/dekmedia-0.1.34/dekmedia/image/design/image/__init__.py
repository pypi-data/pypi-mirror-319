from .const import image_ignore_file
from .node.base import ImageManager
from .node import *
from .res import ImageResManager


def new_image_manager(set_manager):
    return ImageManager(set_manager, ImageResManager(set_manager, [image_ignore_file]))
