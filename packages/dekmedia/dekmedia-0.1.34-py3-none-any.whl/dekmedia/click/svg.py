import os
import asyncio
import typer
from typing_extensions import Annotated
from dektools.file import normal_path

app = typer.Typer(add_completion=False)


@app.command()
def design(src, dest: Annotated[str, typer.Argument()] = ""):
    from ..image.design import SvgSetManager
    src = normal_path(src)
    if os.path.isfile(src):
        src = os.path.dirname(src)
    manager = SvgSetManager()
    manager.load_path(src)
    asyncio.run(manager.dump(dest or os.path.join(src, 'dist')))


@app.callback()
def callback():
    pass
