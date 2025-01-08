from dektools.design.set.base import SetManager
from ..svg import load_svg
from .base.res import get_fonts
from .image import new_image_manager
from .svg import new_svg_manager


class SetMangerDump(SetManager):
    async def dump(self, path):
        await self.manager.dump(path)


class ImageSvgSetManager(SetMangerDump):
    managers = [new_image_manager, new_svg_manager]

    def trans_0_1(self, manager, node, result, args, params, attrs):
        return load_svg(node.manager.final(node, result), attrs.get('width'), attrs.get('height'),
                        fonts=get_fonts(manager.res_manager))


class SvgSetManager(SetMangerDump):
    managers = [new_svg_manager]
