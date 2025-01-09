from dektools.design.res.base import ResBase, ResYaml, ResTypes
from deknetreq.design.apply import ResYamlFuncNet, RpRes, ResManagerNet
from ...base.res import SvgEmbedRes, FontRes

res_types = ResTypes()


@res_types.register
class SvgYamlRes(ResYamlFuncNet):
    ext = ['.svg', '.yaml']


res_types.register(SvgEmbedRes)
res_types.register(RpRes)
res_types.register(FontRes)


class SvgResManager(ResManagerNet):
    types = res_types

    res_cls_setup = SvgYamlRes
