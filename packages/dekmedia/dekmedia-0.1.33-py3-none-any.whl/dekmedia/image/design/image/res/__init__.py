from dektools.design.res.base import ResBase, ResYaml, ResTypes
from deknetreq.design.apply import ResYamlFuncNet, RpRes, ResManagerNet
from ....psd import PsdCanvas
from ...base.res import SvgRes, ImageRes, FontRes

res_types = ResTypes()


@res_types.register
class ImageYamlRes(ResYamlFuncNet):
    ext = ['.image', '.yaml']


@res_types.register
class PsdRes(ResBase):
    ext = '.psd'

    def load(self):
        return PsdCanvas.load(self.path)


@res_types.register
class QrRes(ResYaml):
    ext = ['.qr', '.yaml']


res_types.register(SvgRes)
res_types.register(RpRes)
res_types.register(ImageRes)
res_types.register(FontRes)


class ImageResManager(ResManagerNet):
    types = res_types

    res_cls_setup = ImageYamlRes
