import os
from dektools.file import sure_dir
from dektools.func import FuncAnyArgs
from dektools.design.node.base import NodeBase, NodeTypes
from deknetreq.design.apply import NodeManagerNet
from ....svg import new_svg_manager
from ...res import ImageYamlRes


class NodeImage(NodeBase):
    pass


node_types = NodeTypes()


class ImageManager(NodeManagerNet):
    types = node_types

    res_cls_setup = ImageYamlRes

    new_svg_manager = FuncAnyArgs(new_svg_manager)

    dump_ext = '.png'

    async def dump(self, path):
        def work(file, content):
            p = os.path.join(path, file + self.dump_ext)
            content.save(p)
            self.set_manager.load_path_item(p)

        sure_dir(path)
        if self.has_fetch():
            async for node_name, name, params in self.fetch_items():
                work(name, self.make(node_name, params=params))
        else:
            for name, item in self.entries():
                work(name, item)

    def entries(self, args=None, params=None, attrs=None):
        for name in self.entry_names:
            yield name, self.make(name, args, params, attrs)

    def _translate_assign(self, s, params):
        if s is not None:
            return self.make(s, params=params)
