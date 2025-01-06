import math
from ..base import NodeElement, node_types
from dektools.num import near_zero
from .....svg.utils.path import path_text


class TextPath(NodeElement):
    spec = dict(
        cur=0.0, ac=0.0, g=0.1,
        ff='', fs='', fw='', fy=1.0,
        dy='0.35em',  # equals to "dominant-baseline": "central"
        f='black',
        t='',
    )

    def path(self, proxy):
        raise NotImplementedError()

    def draw(self, proxy):
        texts = {}
        for i, (c, (x, y, a)) in enumerate(path_text(
                self.path(proxy), proxy.t, proxy.cur, proxy.ac, proxy.g * self.width
        )):
            texts["text " + "-" * i] = {
                "dy": proxy.dy,
                "transform": f"translate({x},{y}) rotate({a}) scale(1,{proxy.fy})",
                "+": c
            }
        return {
            "g": {
                "text-anchor": "middle",
                "font-family": proxy.ff,
                "font-size": self.pv(proxy.fs),
                "font-weight": self.pv(proxy.fw),
                "fill": proxy.f,
                "+": texts
            }
        }


@node_types.register
class TextPathCircleNode(TextPath):
    spec = dict(
        **TextPath.spec,
        x=lambda w: w / 2, y=lambda _, h: h / 2,
        a=lambda w: w / 2, b=lambda _, h: h / 2,
        p=1.0,  # percent
    )

    def path(self, proxy):
        rx = proxy.a * proxy.p
        ry = proxy.b * proxy.p
        return (
            f"M{proxy.x} {proxy.y + ry}"
            f"A{rx} {ry} 0 1 1 {proxy.x + rx * math.sin(near_zero)} {proxy.y + ry * math.cos(near_zero)}"
        )
