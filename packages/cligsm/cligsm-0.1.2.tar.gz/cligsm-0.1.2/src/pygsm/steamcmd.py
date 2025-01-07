"""
SteamCMD Manager for server and workshop content installation
"""
import os
import platform
import subprocess
import requests
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

class SteamCMD:
    STEAMCMD_URL = {
        "Linux": "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz",
        "Darwin": "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_osx.tar.gz",
        "Windows": "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"
    }

    def __init__(self, install_path: Path):
        self.install_path = install_path
        self.steamcmd_path = self.install_path / ("steamcmd.exe" if platform.system() == "Windows" else "steamcmd.sh")
        
    def ensure_installed(self):
        """Ensure SteamCMD is installed"""
        if not self.steamcmd_path.exists():
            console.print("[yellow]Installing SteamCMD...[/]")
            self.install_path.mkdir(parents=True, exist_ok=True)
            
            # Download SteamCMD
            response = requests.get(self.STEAMCMD_URL[platform.system()], stream=True)
            archive_path = self.install_path / "steamcmd.tar.gz"
            
            with open(archive_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Extract archive
            if platform.system() == "Windows":
                import zipfile
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(self.install_path)
            else:
                import tarfile
                with tarfile.open(archive_path, 'r:gz') as tar:
                    tar.extractall(self.install_path)
            
            # Make steamcmd executable on Unix
            if platform.system() != "Windows":
                self.steamcmd_path.chmod(0o755)
            
            archive_path.unlink()
            
    def run_command(self, *args: str, user: str = "anonymous", password: str = None):
        """Run a SteamCMD command"""
        self.ensure_installed()
        
        cmd = [str(self.steamcmd_path), "+login", user]
        if password:
            cmd.append(password)
            
        cmd.extend(args)
        cmd.append("+quit")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task("Running SteamCMD...", total=None)
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                console.print(f"[red]Error running SteamCMD: {stderr}[/]")
                raise RuntimeError(f"SteamCMD failed with return code {process.returncode}")
            
            progress.update(task, completed=True)
            
        return stdout
    
    def install_app(self, app_id: str, install_dir: Path, validate: bool = True):
        """Install or update a Steam app"""
        install_dir.mkdir(parents=True, exist_ok=True)
        
        args = [
            f"+force_install_dir {install_dir}",
            f"+app_update {app_id}"
        ]
        
        if validate:
            args.append("validate")
            
        return self.run_command(*args)
    
    def install_workshop_item(self, app_id: str, workshop_id: str, install_dir: Path):
        """Install or update a workshop item"""
        install_dir.mkdir(parents=True, exist_ok=True)
        
        args = [
            f"+force_install_dir {install_dir}",
            f"+workshop_download_item {app_id} {workshop_id}"
        ]
        
        return self.run_command(*args) 