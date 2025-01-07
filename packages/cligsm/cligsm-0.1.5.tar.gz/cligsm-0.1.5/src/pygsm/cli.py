"""
Command-line interface for PyGSM
"""
import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from .config import get_server_path
from .servers.arma3.arma3 import Arma3Server

console = Console()

@click.group()
@click.version_option()
def main():
    """CLIGSM - Game Server Management Made Easy"""
    pass

@main.group()
def arma3():
    """Manage Arma 3 servers"""
    pass

@arma3.command()
@click.argument('name')
@click.option('--port', default=2302, help='Server port')
@click.option('--max-players', default=32, help='Maximum number of players')
@click.option('--password', default='', help='Server password')
@click.option('--admin-password', default='', help='Admin password')
@click.option('--mods-html', type=click.Path(exists=True), help='Path to Arma 3 launcher mods HTML export')
@click.option('--server-mods-html', type=click.Path(exists=True), help='Path to server-side mods HTML export')
def create(name, port, max_players, password, admin_password, mods_html, server_mods_html):
    """Create a new Arma 3 server"""
    server_path = get_server_path(f"arma3_{name}")
    server = Arma3Server(name, server_path)
    
    server.port = port
    server.max_players = max_players
    server.password = password
    server.admin_password = admin_password
    
    if mods_html:
        console.print(f"[yellow]Loading mods from {mods_html}[/]")
        server.load_mods_from_html(Path(mods_html))
        
    if server_mods_html:
        console.print(f"[yellow]Loading server mods from {server_mods_html}[/]")
        server.load_mods_from_html(Path(server_mods_html), server_mods=True)
    
    server.save_config()
    server.install()
    
    console.print(f"[green]Arma 3 server '{name}' created successfully![/]")

@arma3.command()
@click.argument('name')
@click.option('--monitor', is_flag=True, help='Show live performance monitoring')
def start(name, monitor):
    """Start an Arma 3 server"""
    server_path = get_server_path(f"arma3_{name}")
    server = Arma3Server(name, server_path)
    server.load_config()
    server.start()
    
    if monitor:
        server.monitor.show_live_stats()

@arma3.command()
@click.argument('name')
def stop(name):
    """Stop an Arma 3 server"""
    server_path = get_server_path(f"arma3_{name}")
    server = Arma3Server(name, server_path)
    server.stop()

@arma3.command()
@click.argument('name')
def status(name):
    """Show Arma 3 server status and configuration"""
    server_path = get_server_path(f"arma3_{name}")
    server = Arma3Server(name, server_path)
    server.load_config()
    
    table = Table(title=f"Arma 3 Server: {name}")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Server Name", server.server_name)
    table.add_row("Port", str(server.port))
    table.add_row("Max Players", str(server.max_players))
    table.add_row("Password Protected", "Yes" if server.password else "No")
    table.add_row("BattlEye", "Enabled" if server.battle_eye else "Disabled")
    table.add_row("Mods Count", str(len(server.mods)))
    table.add_row("Server Mods Count", str(len(server.server_mods)))
    
    console.print(table)
    
    if server.mods:
        console.print("\n[yellow]Loaded Mods:[/]")
        for mod in server.mods:
            console.print(f"  • {mod.name} ({mod.path})")
            
    if server.server_mods:
        console.print("\n[yellow]Server Mods:[/]")
        for mod in server.server_mods:
            console.print(f"  • {mod.name} ({mod.path})")
            
    if server.monitor:
        console.print("\n[cyan]Performance Statistics:[/]")
        console.print(server.monitor.get_current_stats())

@arma3.command()
@click.argument('name')
def update(name):
    """Update server and all mods"""
    server_path = get_server_path(f"arma3_{name}")
    server = Arma3Server(name, server_path)
    server.load_config()
    server.update()

@arma3.group()
def mission():
    """Manage server missions"""
    pass

@mission.command()
@click.argument('server_name')
@click.argument('mission_path', type=click.Path(exists=True))
def install(server_name, mission_path):
    """Install a mission file or directory"""
    server_path = get_server_path(f"arma3_{server_name}")
    server = Arma3Server(server_name, server_path)
    server.mission_manager.install_mission(Path(mission_path))

@mission.command()
@click.argument('server_name')
def list(server_name):
    """List installed missions"""
    server_path = get_server_path(f"arma3_{server_name}")
    server = Arma3Server(server_name, server_path)
    
    missions = server.mission_manager.list_missions()
    
    table = Table(title="Installed Missions")
    table.add_column("Name", style="cyan")
    table.add_column("Type", style="green")
    
    for mission in missions:
        table.add_row(mission.name, mission.metadata["type"])
        
    console.print(table)

@arma3.group()
def backup():
    """Manage server backups"""
    pass

@backup.command()
@click.argument('server_name')
@click.option('--name', help='Custom backup name')
def create(server_name, name):
    """Create a server backup"""
    server_path = get_server_path(f"arma3_{server_name}")
    server = Arma3Server(server_name, server_path)
    server.backup_manager.create_backup(name)

@backup.command()
@click.argument('server_name')
@click.argument('backup_name')
def restore(server_name, backup_name):
    """Restore from a backup"""
    server_path = get_server_path(f"arma3_{server_name}")
    server = Arma3Server(server_name, server_path)
    
    backup_path = server.backup_manager.backup_dir / f"{backup_name}.zip"
    server.backup_manager.restore_backup(backup_path)

@backup.command()
@click.argument('server_name')
def list(server_name):
    """List available backups"""
    server_path = get_server_path(f"arma3_{server_name}")
    server = Arma3Server(server_name, server_path)
    
    backups = server.backup_manager.list_backups()
    
    table = Table(title="Server Backups")
    table.add_column("Name", style="cyan")
    table.add_column("Date", style="green")
    table.add_column("Size", style="yellow")
    
    for backup in backups:
        size_mb = backup["size"] / 1024 / 1024
        table.add_row(
            backup["name"],
            backup["timestamp"],
            f"{size_mb:.1f} MB"
        )
        
    console.print(table)

if __name__ == '__main__':
    main() 