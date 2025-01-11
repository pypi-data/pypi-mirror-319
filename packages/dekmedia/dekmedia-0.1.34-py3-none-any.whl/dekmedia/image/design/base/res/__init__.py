from PIL import Image
from dektools.design.res.base import ResBase, ResText, ResBytes
from dektools.ext.font import font_extensions
from dektools.ext.image import image_extensions


class SvgEmbedRes(ResText):
    ext = '.svg'


class SvgRes(ResBytes):
    ext = '.svg'


class ImageRes(ResBase):
    ext = image_extensions

    def load(self):
        return Image.open(self.path)


class FontRes(ResBase):
    ext = font_extensions


def get_fonts(res_manager):
    fonts = res_manager.get_res_map(FontRes.get_typed()) or {}
    if fonts:
        return {k: {'font_path': v.path} for k, v in fonts.items()}
