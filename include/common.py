import rich
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.markdown import Markdown

#style="grey", style="bold blue", style="italic yellow", style="underline green".
#border_style="bold red", border_style="#FF5733", or border_style="cyan".
#box=rich.box.ROUNDED, box=rich.box.SQUARE, box=rich.box.MINIMAL
console = Console()

def resp(msg, title):
    console.print(Panel(msg, title=title, title_align="left", border_style="cyan", 
                    style="#FF5733", box=rich.box.ROUNDED))
def promp(msg, title):
    console.print(Panel(msg, title=title, title_align="left", border_style="white", style="underline green", 
                    box=rich.box.MINIMAL, highlight=True))