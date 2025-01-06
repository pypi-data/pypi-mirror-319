from .node.base import ImageManager
from .res.base import ImageResManager
from .node import *
from .res import *
from .const import image_ignore_file


def new_image_manager(set_manager):
    return ImageManager(set_manager, ImageResManager(set_manager, [image_ignore_file]))
