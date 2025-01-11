from dektools.design.base import split_function
from dektools.dict import assign_list
from .base import NodeCanvas, NodeSvg, node_types
from .elements import *


@node_types.register
class FunctionNode(NodeCanvas):
    def make(self, args, params, attrs):
        _args, _params, body = self.res.content
        params = self.merge_params(_params, params)
        args = self.merge_args(_args, args, params)
        wh = assign_list([self.manager.default_width, self.manager.default_height], args)
        result = ""
        for key, value in body.items():
            _args, _params, _body = split_function(value)
            params = self.merge_params(_params, params)
            args = self.merge_args(_args, args, params)
            attrs = self.manager.translate_map(_body, params)
            name, trans = self.manager.parse_call_label(params, key, self)
            result += self.manager.make(
                name, args, params, attrs,
                init=lambda n: n.set_wh(*wh) if isinstance(n, NodeCanvas) else None,
                final=lambda n, r: f"""<g{trans}>{r}</g>""" if trans or n.need_g_wrapper else r
            )
        return result


@node_types.register
class SvgEmbedNode(NodeSvg):
    need_g_wrapper = True

    def make(self, args, params, attrs):
        if attrs:
            return self.manager.render_by_struct({'g': {**attrs, '+': self.res.content}}, params)
        return self.res.content


@node_types.register
class UnknownNode(NodeSvg):
    def make(self, args, params, attrs):
        return self.manager.render_by_struct({self.res.name: attrs}, params)
