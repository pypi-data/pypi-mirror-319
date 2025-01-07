import sys
import typer
import re
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich import print as rprint
from typing import Optional
from dataclasses import dataclass
from .about import __version__

app: typer.Typer = typer.Typer(help=f"D15 command line interface. (v{__version__})")
console = Console()


def sanitize_filename(text: str, max_length: int = 50) -> str:
    """Sanitize text for use in filenames, truncating if needed."""
    # Replace spaces with underscores and remove problematic characters
    clean = re.sub(r'[<>:"/\\|?*]', "", text.replace(" ", "_"))
    # Truncate to max_length while keeping whole words where possible
    if len(clean) > max_length:
        clean = clean[:max_length].rsplit("_", 1)[0]
    return clean.strip("_")


@dataclass
class RenderConfig:
    height: int = 768
    width: int = 768
    steps: int = 30
    seed: Optional[int] = None
    output_dir: Path = Path("outputs")
    base64: bool = False


class D15Repl:
    def __init__(self):
        self.config = RenderConfig()
        self.pipeline = None

    def load_pipeline(self):
        """Lazy load the pipeline only when needed"""
        if self.pipeline is None:
            with console.status("[bold green]Loading D15 pipeline..."):
                from .render import MaskedStableDiffusionPipeline
                import torch

                device = "cuda" if torch.cuda.is_available() else "cpu"
                self.pipeline = MaskedStableDiffusionPipeline.from_pretrained(
                    "justin/d15"
                ).to(device, dtype=torch.bfloat16)

    def show_status(self):
        table = Table(title="D15 Configuration")
        table.add_column("Parameter", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Width", str(self.config.width))
        table.add_row("Height", str(self.config.height))
        table.add_row("Steps", str(self.config.steps))
        table.add_row("Seed", str(self.config.seed))
        table.add_row("Output Directory", str(self.config.output_dir))
        table.add_row("Base64 Output", str(self.config.base64))

        console.print(table)

    def help(self):
        help_text = """
        Commands:
        /render <prompt>  - Generate an image
        /width N         - Set width to N
        /height N        - Set height to N
        /steps N         - Set number of steps
        /seed N         - Set seed (use 'none' to randomize)
        /size WxH       - Set both width and height
        /dir path       - Set output directory
        /base64         - Toggle base64 output
        /status         - Show current configuration
        /help           - Show this help
        /exit          - Exit the REPL
        """
        console.print(Panel(help_text, title="D15 REPL Help", border_style="green"))

    def handle_command(self, cmd: str) -> bool:
        """Handle a command. Return False to exit the REPL."""
        if not cmd:
            return True

        parts = cmd.split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if command == "/exit":
            return False
        elif command == "/help":
            self.help()
        elif command == "/status":
            self.show_status()
        elif command == "/width":
            try:
                self.config.width = int(args)
                rprint(f"[green]Width set to {self.config.width}")
            except ValueError:
                rprint("[red]Invalid width value")
        elif command == "/height":
            try:
                self.config.height = int(args)
                rprint(f"[green]Height set to {self.config.height}")
            except ValueError:
                rprint("[red]Invalid height value")
        elif command == "/size":
            try:
                w, h = map(int, args.lower().split("x"))
                self.config.width = w
                self.config.height = h
                rprint(f"[green]Size set to {w}x{h}")
            except:
                rprint("[red]Invalid size format. Use WxH (e.g. 768x512)")
        elif command == "/steps":
            try:
                self.config.steps = int(args)
                rprint(f"[green]Steps set to {self.config.steps}")
            except ValueError:
                rprint("[red]Invalid steps value")
        elif command == "/seed":
            if args.lower() == "none":
                self.config.seed = None
                rprint("[green]Seed set to random")
            else:
                try:
                    self.config.seed = int(args)
                    rprint(f"[green]Seed set to {self.config.seed}")
                except ValueError:
                    rprint("[red]Invalid seed value")
        elif command == "/base64":
            self.config.base64 = not self.config.base64
            rprint(
                f"[green]Base64 output {'enabled' if self.config.base64 else 'disabled'}"
            )
        elif command == "/render":
            if not args:
                rprint("[red]Please provide a prompt")
                return True
            self.render(args)
        else:
            # Treat as render command if doesn't start with /
            if not command.startswith("/"):
                self.render(cmd)
            else:
                rprint(f"[red]Unknown command: {command}")
                rprint("[yellow]Type /help for available commands")

        return True

    def render(self, prompt: str):
        try:
            from .render import d15_render

            with console.status("[bold green]Generating image..."):
                image = d15_render(
                    prompt,
                    height=self.config.height,
                    width=self.config.width,
                    steps=self.config.steps,
                    seed=self.config.seed,
                )

            if self.config.base64:
                import base64
                from io import BytesIO

                buffered = BytesIO()
                image.save(buffered, format="PNG")
                result = base64.b64encode(buffered.getvalue()).decode("utf-8")
                console.print(result)
            else:
                self.config.output_dir.mkdir(parents=True, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                seed_str = (
                    f"{self.config.seed:08d}"
                    if self.config.seed is not None
                    else "random"
                )
                sanitized_prompt = sanitize_filename(prompt)
                filename = f"{timestamp}_{seed_str}_{sanitized_prompt}.png"
                output_path = self.config.output_dir / filename
                image.save(output_path)
                console.print(f"[green]Saved image to: {output_path}")

        except Exception as e:
            console.print(f"[red]Error generating image: {str(e)}")

    def run(self):
        console.print(
            Panel.fit(
                "Welcome to D15 REPL! Type /help for commands, /exit to quit",
                title="D15 v" + __version__,
                border_style="green",
            )
        )
        self.show_status()

        while True:
            try:
                cmd = Prompt.ask("\n[bold green]D15[/bold green]").strip()
                if not self.handle_command(cmd):
                    break
            except KeyboardInterrupt:
                console.print("\n[yellow]Use /exit to quit")
            except Exception as e:
                console.print(f"[red]Error: {str(e)}")


@app.command()
def repl():
    """Start an interactive REPL session"""
    D15Repl().run()


# Keep the existing render command
@app.command()
def render(
    text: str,
    output_dir: Path = typer.Option(
        Path("outputs"), "--dir", "-d", help="Directory to save generated images"
    ),
    base64: bool = typer.Option(
        False,
        "--base64",
        "-b",
        help="Output base64 encoded image instead of saving to file",
    ),
    seed: int | None = typer.Option(
        None, "--seed", "-s", help="Random seed for generation"
    ),
) -> str:
    """Render an image from a given text string."""
    repl = D15Repl()
    repl.config.output_dir = output_dir
    repl.config.base64 = base64
    repl.config.seed = seed
    repl.render(text)


def cli():
    """Entry point that defaults to REPL if no command is given"""
    if len(sys.argv) == 1:
        repl()
    else:
        app()


if __name__ == "__main__":
    cli()

__all__ = ()
