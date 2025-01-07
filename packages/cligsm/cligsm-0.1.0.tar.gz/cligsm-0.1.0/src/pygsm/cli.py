"""
Command-line interface for PyGSM
"""
import click
from rich.console import Console
from rich.panel import Panel

console = Console()

@click.group()
@click.version_option()
def main():
    """PyGSM - Game Server Management Made Easy"""
    pass

@main.command()
@click.argument('game')
def install(game):
    """Install a game server"""
    console.print(Panel.fit(f"Installing {game} server..."))

@main.command()
@click.argument('game')
def start(game):
    """Start a game server"""
    console.print(Panel.fit(f"Starting {game} server..."))

@main.command()
@click.argument('game')
def stop(game):
    """Stop a game server"""
    console.print(Panel.fit(f"Stopping {game} server..."))

@main.command()
def status():
    """Check status of all servers"""
    console.print(Panel.fit("Checking server status..."))

if __name__ == '__main__':
    main() 