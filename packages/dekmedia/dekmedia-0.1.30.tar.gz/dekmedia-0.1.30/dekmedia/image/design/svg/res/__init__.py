from deknetreq.design.apply import ResYamlFuncNet, RpRes
from ...base.res import SvgEmbedRes, FontRes
from .base import res_types


@res_types.register
class SvgYamlRes(ResYamlFuncNet):
    ext = ['.svg', '.yaml']


res_types.register(SvgEmbedRes)
res_types.register(RpRes)
res_types.register(FontRes)
