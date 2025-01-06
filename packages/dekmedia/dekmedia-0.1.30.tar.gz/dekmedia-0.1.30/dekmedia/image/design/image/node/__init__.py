import qrcode
from PIL import Image
from qrcode.image.styledpil import StyledPilImage
from skimage.io._plugins.pil_plugin import pil_to_ndarray, ndarray_to_pil
from dektools.module import get_module_attr
from dektools.design.base import split_function
from dektools.dict import assign
from ....svg import load_svg
from ...base.res import get_fonts
from .base import NodeImage, node_types


@node_types.register
class FunctionNode(NodeImage):
    module_image_operations = (
        (f'{__name__}.operations.image', False),
        f'{__name__}.operations.array',
        'skimage',
        'numpy',
        ('PIL.ImageOps', False)
    )

    def make(self, args, params, attrs):
        _args, _params, body = self.res.content
        params = self.merge_params(_params, params)
        args = self.merge_args(_args, args, params)
        image = None
        for index, (name, value) in enumerate(body.items()):
            _args, _params, _body = split_function(value)
            params = self.merge_params(_params, params)
            args = self.merge_args(_args, args, params)
            attrs = self.manager.translate_map(_body, params)
            if index == 0:
                image = self.manager.make(name, args, params, attrs)
            else:
                name = name.rstrip('+')
                func = None
                is_na = True
                for m in self.module_image_operations:
                    if isinstance(m, str):
                        is_na = True
                    else:
                        m, is_na = m
                    try:
                        func = get_module_attr(f'{m}.{name}')
                        break
                    except (ModuleNotFoundError, AttributeError):
                        pass
                if func is None:
                    is_na = False
                    func = getattr(Image.Image, name, None)
                if func is None:
                    raise AttributeError(f"Can't find func: {name}")
                if is_na:
                    if isinstance(image, Image.Image):
                        image = pil_to_ndarray(image)
                else:
                    if not isinstance(image, Image.Image):
                        image = ndarray_to_pil(image)
                image = func(image, *args, **attrs)

        if not isinstance(image, Image.Image):
            return ndarray_to_pil(image)
        return image


@node_types.register
class SvgNode(NodeImage):
    def make(self, args, params, attrs):
        return load_svg(self.res.content, attrs.get('width'), attrs.get('height'),
                        fonts=get_fonts(self.manager.res_manager))


@node_types.register
class ImageNode(NodeImage):
    def make(self, args, params, attrs):
        return self.res.content


@node_types.register
class PsdNode(NodeImage):
    def make(self, args, params, attrs):
        self.res.content.update(attrs)
        return self.res.content.render()


@node_types.register
class QrNode(NodeImage):
    default_props = {
        'version': 1,
        'error': qrcode.constants.ERROR_CORRECT_L,
        'box': 10,
        'border': 0,
        'color': 'black',
        'bgc': 'white',
        'embed': None,
        'fit': True
    }

    def make(self, args, params, attrs):
        props = assign(self.default_props, attrs, self.manager.translate_map(self.res.content or {}, params))
        qr = qrcode.QRCode(
            version=props['version'],
            error_correction=props['error'],
            box_size=props['box'],
            border=props['border'],
        )
        qr.add_data(props['text'])
        qr.make(fit=props['fit'])
        return qr.make_image(
            fill_color=props['color'],
            back_color=props['bgc'],
            image_factory=StyledPilImage,
            embeded_image=props['embed'] or None
        )
