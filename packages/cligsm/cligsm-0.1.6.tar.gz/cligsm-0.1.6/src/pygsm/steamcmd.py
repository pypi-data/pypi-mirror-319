"""
SteamCMD Manager for server and workshop content installation
"""
import os
import platform
import subprocess
import requests
import shutil
import getpass
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

    LINUX_DEPENDENCIES = [
        "lib32gcc-s1",      # For Ubuntu 22.04+
        "lib32gcc1",        # For older Ubuntu versions
        "lib32stdc++6",
        "libsdl2-2.0-0:i386",
        "libtinfo5:i386",
        "lib32z1",
        "libstdc++6:i386",
        "libtinfo6:i386",
        "libcurl4:i386",
        "libsdl2-2.0-0:i386",
        "libtcmalloc-minimal4:i386",
        "libncurses6:i386",
        "libncurses5:i386",
        "ca-certificates"    # For HTTPS downloads
    ]

    def __init__(self, install_path: Path):
        self.install_path = install_path
        self.steamcmd_path = self.install_path / ("steamcmd.exe" if platform.system() == "Windows" else "steamcmd.sh")
        
    def _run_sudo_command(self, cmd: list, check: bool = True, env: dict = None) -> subprocess.CompletedProcess:
        """Run a command with sudo if needed"""
        try:
            # Try running without sudo first
            return subprocess.run(cmd, check=check, capture_output=True, text=True, env=env)
        except (subprocess.CalledProcessError, PermissionError):
            # If it fails, try with sudo
            sudo_cmd = ["sudo", "-E"] if env else ["sudo"]
            sudo_cmd.extend(cmd)
            return subprocess.run(sudo_cmd, check=check, capture_output=True, text=True, env=env)
        
    def _check_linux_dependencies(self):
        """Check and install required Linux dependencies"""
        if platform.system() != "Linux":
            return

        console.print("[yellow]Checking system dependencies...[/]")
        
        try:
            # Enable 32-bit architecture
            console.print("[yellow]Enabling 32-bit architecture support...[/]")
            self._run_sudo_command(["dpkg", "--add-architecture", "i386"])
            
            # Update package lists
            console.print("[yellow]Updating package lists...[/]")
            self._run_sudo_command(["apt-get", "update", "-y"])
            
            # Install all dependencies at once first
            try:
                console.print("[yellow]Installing dependencies...[/]")
                self._run_sudo_command(["apt-get", "install", "-y", "--no-install-recommends"] + self.LINUX_DEPENDENCIES)
            except subprocess.CalledProcessError:
                # If bulk install fails, try one by one
                console.print("[yellow]Some packages failed to install, trying individually...[/]")
                for dep in self.LINUX_DEPENDENCIES:
                    try:
                        self._run_sudo_command(["apt-get", "install", "-y", "--no-install-recommends", dep])
                    except subprocess.CalledProcessError as e:
                        console.print(f"[yellow]Warning: Failed to install {dep}, continuing...[/]")
            
        except subprocess.CalledProcessError as e:
            console.print("[red]Error installing dependencies:[/]")
            console.print(e.stderr)
            raise RuntimeError("Failed to install system dependencies") from e
        
    def ensure_installed(self):
        """Ensure SteamCMD is installed"""
        if not self.steamcmd_path.exists():
            console.print("[yellow]Installing SteamCMD...[/]")
            
            # Check system dependencies first
            if platform.system() == "Linux":
                self._check_linux_dependencies()
            
            self.install_path.mkdir(parents=True, exist_ok=True)
            
            # Download SteamCMD
            console.print("[yellow]Downloading SteamCMD...[/]")
            response = requests.get(self.STEAMCMD_URL[platform.system()], stream=True)
            archive_path = self.install_path / "steamcmd.tar.gz"
            
            with open(archive_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Extract archive
            console.print("[yellow]Extracting SteamCMD...[/]")
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
                
                # Create linux32 directory
                linux32_dir = self.install_path / "linux32"
                linux32_dir.mkdir(exist_ok=True)
                
                # Copy steamcmd to linux32 directory
                steamcmd_bin = linux32_dir / "steamcmd"
                if not steamcmd_bin.exists():
                    shutil.copy2(self.steamcmd_path, steamcmd_bin)
                    steamcmd_bin.chmod(0o755)
            
            archive_path.unlink()
            
            # Run steamcmd once to install updates and verify
            self._initial_setup()
            
    def _initial_setup(self):
        """Run initial SteamCMD setup"""
        console.print("[yellow]Running initial SteamCMD setup...[/]")
        env = {
            "LD_LIBRARY_PATH": str(self.install_path / "linux32"),
            "HOME": str(Path.home()),
            "PATH": os.environ.get("PATH", ""),
            "TERM": os.environ.get("TERM", "xterm")
        }
        
        try:
            # First, try to fix any Steam installation issues
            subprocess.run(
                [str(self.steamcmd_path), "+login", "anonymous", "+quit"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env
            )
        except subprocess.CalledProcessError as e:
            console.print("[red]Error during initial SteamCMD setup:[/]")
            console.print(e.stderr)
            
            # Try to repair the installation
            console.print("[yellow]Attempting to repair SteamCMD installation...[/]")
            try:
                repair_cmd = [str(self.steamcmd_path), "+login", "anonymous", "+app_update", "7", "validate", "+quit"]
                subprocess.run(repair_cmd, check=True, env=env)
            except subprocess.CalledProcessError:
                # Try one more time with a clean installation
                console.print("[yellow]Attempting clean installation...[/]")
                shutil.rmtree(self.install_path)
                self.install_path.mkdir(parents=True)
                self.ensure_installed()
            
    def run_command(self, *args: str, user: str = "anonymous", password: str = None):
        """Run a SteamCMD command"""
        self.ensure_installed()
        
        cmd = [str(self.steamcmd_path), "+login", user]
        if password:
            cmd.append(password)
            
        cmd.extend(args)
        cmd.append("+quit")
        
        env = {
            "LD_LIBRARY_PATH": str(self.install_path / "linux32"),
            "HOME": str(Path.home()),
            "PATH": os.environ.get("PATH", ""),
            "TERM": os.environ.get("TERM", "xterm")
        }
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task("Running SteamCMD...", total=None)
            try:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    env=env
                )
                stdout, stderr = process.communicate()
                
                if process.returncode != 0:
                    console.print(f"[red]Error running SteamCMD:[/]")
                    console.print(f"[red]Command: {' '.join(cmd)}[/]")
                    console.print(f"[red]Error: {stderr}[/]")
                    console.print(f"[red]Output: {stdout}[/]")
                    
                    # Try to recover from common errors
                    if "cannot execute: required file not found" in stderr:
                        console.print("[yellow]Attempting to repair SteamCMD installation...[/]")
                        self._initial_setup()
                        # Retry the command
                        return self.run_command(*args, user=user, password=password)
                    
                    raise RuntimeError(f"SteamCMD failed with return code {process.returncode}")
                
                progress.update(task, completed=True)
                
            except FileNotFoundError:
                console.print("[red]Error: SteamCMD executable not found. Attempting reinstallation...[/]")
                shutil.rmtree(self.install_path, ignore_errors=True)
                self.ensure_installed()
                return self.run_command(*args, user=user, password=password)
            
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