import typer
import asyncio
from scrapybara import Scrapybara
from dotenv import load_dotenv
from rich.console import Console
from rich import print
import os
from getpass import getpass
from .helpers import ToolCollection
from scrapybara.anthropic import ComputerTool, BashTool, EditTool
from .agent import run_agent

load_dotenv()

console = Console()
app = typer.Typer()


@app.command()
def main(
    instance_type: str = typer.Option(
        "small", help="Size of the instance. Must be one of: 'small', 'medium', 'large'"
    )
):
    """
    Run the CLI-based computer agent, powered by Scrapybara and Anthropic!
    """
    # Check for required environment variables
    scrapybara_key = os.getenv("SCRAPYBARA_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if not scrapybara_key:
        scrapybara_key = getpass("Please enter your Scrapybara API key: ").strip()
        os.environ["SCRAPYBARA_API_KEY"] = scrapybara_key
        if not scrapybara_key:
            raise typer.BadParameter("Scrapybara API key is required to continue.")

    if not anthropic_key:
        anthropic_key = getpass("Please enter your Anthropic API key: ").strip()
        os.environ["ANTHROPIC_API_KEY"] = anthropic_key
        if not anthropic_key:
            raise typer.BadParameter("Anthropic API key is required to continue.")

    if instance_type not in ["small", "medium", "large"]:
        raise typer.BadParameter(
            'instance_type must be one of: "small", "medium", "large"'
        )

    # Initialize Scrapybara with the API key
    scrapybara = Scrapybara(api_key=scrapybara_key)

    asyncio.run(async_main(instance_type, scrapybara))


async def async_main(instance_type: str, scrapybara: Scrapybara):
    try:
        with console.status(
            "[bold green]Starting instance...[/bold green]", spinner="dots"
        ) as status:
            instance = scrapybara.start(instance_type=instance_type)
            status.update("[bold green]Instance started![/bold green]")

        stream_url = instance.get_stream_url().stream_url
        print(
            f"[bold blue]Stream URL: {stream_url}/?resize=scale&autoconnect=1[/bold blue]"
        )

        tools = ToolCollection(
            ComputerTool(instance),
            BashTool(instance),
            EditTool(instance),
        )

        while True:
            prompt = input("> ")
            await run_agent(instance, tools, prompt)

    except Exception as e:
        print(f"[bold red]{e}[/bold red]")

    finally:
        with console.status(
            "[bold red]Stopping instance...[/bold red]", spinner="dots"
        ) as status:
            instance.stop()
            status.update("[bold red]Instance stopped![/bold red]")


if __name__ == "__main__":
    app()
