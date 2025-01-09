import os
import asyncio
import typer
from typing import List
from typing_extensions import Annotated
from dektools.file import read_file, normal_path
from . import svg as svg_command

app = typer.Typer(add_completion=False)
app.add_typer(svg_command.app, name='svg')


@app.command()
def trans(src, outputs: Annotated[List[str], typer.Argument()] = None, sizes=''):
    if not outputs:
        return
    if os.path.splitext(src)[-1].lower() == '.svg':
        from ..image.svg import load_svg
        image = load_svg(read_file(src))
    else:
        from PIL import Image
        image = Image.open(src)
    from ..image.core import resize_image
    resize_image(image, outputs, parse_sizes(sizes))


def parse_sizes(sizes):
    if sizes:
        ss = [int(n) for n in sizes.split(',')]
        return list(zip(ss[::2], ss[1::2]))


@app.command()
def psd(src, dest: Annotated[str, typer.Argument()] = ""):
    from ..image.psd import PsdCanvas
    src = normal_path(src)
    dest = dest if dest else os.path.join(src + '.dump')
    pc = PsdCanvas.load(src)
    pc.dump(dest)


@app.command()
def design(src, dest: Annotated[str, typer.Argument()] = ""):
    src = normal_path(src)
    if os.path.isfile(src):
        src = os.path.dirname(src)
    from ..image.design import ImageSvgSetManager
    manager = ImageSvgSetManager()
    manager.load_path(src)
    asyncio.run(manager.dump(dest or src))
