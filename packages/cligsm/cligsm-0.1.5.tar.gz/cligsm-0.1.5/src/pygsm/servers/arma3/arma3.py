"""
Arma 3 Server Management Module
"""
from dataclasses import dataclass
from pathlib import Path
import json
import re
import subprocess
import shutil
import zipfile
import configparser
from typing import List, Optional, Dict
from ...server import GameServer
from ...steamcmd import SteamCMD
from ...monitor import ServerMonitor
from ...backup import BackupManager
from rich.console import Console

console = Console()

@dataclass
class Arma3Mission:
    name: str
    path: Path
    is_pbo: bool
    metadata: Dict

    @classmethod
    def from_path(cls, path: Path) -> 'Arma3Mission':
        """Create mission from path"""
        is_pbo = path.suffix.lower() == '.pbo'
        metadata = cls._read_metadata(path)
        return cls(
            name=path.stem,
            path=path,
            is_pbo=is_pbo,
            metadata=metadata
        )

    @staticmethod
    def _read_metadata(path: Path) -> Dict:
        """Read mission metadata"""
        metadata = {
            "name": path.stem,
            "type": "pbo" if path.suffix.lower() == '.pbo' else "directory",
            "description": "",
            "author": "",
            "min_players": 1,
            "max_players": 0
        }

        if path.is_dir():
            # Try to read mission.sqm
            sqm_path = path / "mission.sqm"
            if sqm_path.exists():
                try:
                    config = configparser.ConfigParser()
                    with open(sqm_path, 'r', encoding='utf-8') as f:
                        content = '[mission]\n' + f.read()
                        config.read_string(content)
                    
                    if 'mission' in config:
                        mission = config['mission']
                        metadata.update({
                            "description": mission.get('briefingName', ''),
                            "author": mission.get('author', ''),
                            "min_players": mission.getint('minPlayers', 1),
                            "max_players": mission.getint('maxPlayers', 0)
                        })
                except Exception as e:
                    console.print(f"[yellow]Warning: Could not read mission.sqm: {e}[/]")

        return metadata

@dataclass
class Arma3Mod:
    name: str
    path: str
    workshop_id: Optional[str] = None
    required: bool = True

    @classmethod
    def from_html(cls, html_path: Path) -> List['Arma3Mod']:
        """Parse Arma 3 mod HTML file to get mod information"""
        mods = []
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract mod information from HTML
            mod_entries = re.findall(r'<td data-type="DisplayName">(.*?)</td>.*?<td data-type="Link">(.*?)</td>', 
                                   content, re.DOTALL)
            for name, link in mod_entries:
                workshop_id = re.search(r'id=(\d+)', link)
                mods.append(cls(
                    name=name.strip(),
                    path=f"@{name.strip().lower().replace(' ', '_')}",
                    workshop_id=workshop_id.group(1) if workshop_id else None
                ))
        return mods

class Arma3Server(GameServer):
    ARMA3_APP_ID = "233780"
    DEFAULT_CONFIG = {
        "server": {
            "hostname": "CLIGSM Arma 3 Server",
            "password": "",
            "passwordAdmin": "",
            "maxPlayers": 32,
            "persistent": 1,
            "battleye": 1,
            "verifySignatures": 2,
            "kickDuplicate": 1,
            "allowedFilePatching": 0,
            "vonCodecQuality": 10,
            "disableVoN": 0,
            "vonCodec": 1,
            "motd[]": [
                "Welcome to CLIGSM Arma 3 Server",
                "Enjoy your stay!"
            ],
            "admins[]": []
        },
        "network": {
            "MaxMsgSend": 128,
            "MaxSizeGuaranteed": 512,
            "MaxSizeNonguaranteed": 256,
            "MinBandwidth": 131072,
            "MaxBandwidth": 2097152,
            "MaxSendPacketSize": 1024,
            "MaxPacketSize": 1400,
            "MinErrorToSend": 0.001,
            "MinErrorToSendNear": 0.01
        }
    }
    
    def __init__(self, name: str, path: Path):
        super().__init__(
            name=name,
            path=str(path),
            executable="arma3server_x64"
        )
        self.config_dir = path / "cfg"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.missions_dir = path / "mpmissions"
        self.missions_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize managers
        self.steamcmd = SteamCMD(path / "steamcmd")
        self.backup_manager = BackupManager(path, path / "backups")
        self.monitor: Optional[ServerMonitor] = None
        
        self.mods: List[Arma3Mod] = []
        self.server_mods: List[Arma3Mod] = []
        self.active_mission: Optional[Arma3Mission] = None
        
        # Default settings
        self.port = 2302
        self.max_players = 32
        self.server_name = "CLIGSM Arma 3 Server"
        self.password = ""
        self.admin_password = ""
        self.battle_eye = True
        
    def load_mods_from_html(self, html_path: Path, server_mods: bool = False):
        """Load mods from Arma 3 launcher HTML export"""
        mods = Arma3Mod.from_html(html_path)
        if server_mods:
            self.server_mods.extend(mods)
        else:
            self.mods.extend(mods)
            
    def generate_config(self):
        """Generate server configuration files"""
        # Update default config with current settings
        config = self.DEFAULT_CONFIG.copy()
        config["server"].update({
            "hostname": self.server_name,
            "password": self.password,
            "passwordAdmin": self.admin_password,
            "maxPlayers": self.max_players,
            "battleye": int(self.battle_eye)
        })
        
        # Server config
        with open(self.config_dir / "server.cfg", 'w') as f:
            for section, values in config.items():
                if section == "server":
                    for key, value in values.items():
                        if isinstance(value, list):
                            for item in value:
                                f.write(f'{key} = "{item}";\n')
                        elif isinstance(value, str):
                            f.write(f'{key} = "{value}";\n')
                        else:
                            f.write(f'{key} = {value};\n')
        
        # Network config
        with open(self.config_dir / "network.cfg", 'w') as f:
            for key, value in config["network"].items():
                f.write(f'{key} = {value};\n')
                
    def get_launch_parameters(self) -> List[str]:
        """Get server launch parameters"""
        params = [
            f"-ip=0.0.0.0",
            f"-port={self.port}",
            f"-config={self.config_dir}/server.cfg",
            f"-cfg={self.config_dir}/network.cfg",
            "-autoinit",
            "-loadmissiontomemory"
        ]
        
        if self.mods:
            mod_paths = [str(Path("mods") / mod.path) for mod in self.mods]
            params.append(f"-mod={';'.join(mod_paths)}")
            
        if self.server_mods:
            servermod_paths = [str(Path("mods") / mod.path) for mod in self.server_mods]
            params.append(f"-serverMod={';'.join(servermod_paths)}")
            
        if self.active_mission:
            params.append(f"-mission={self.active_mission.path.relative_to(Path(self.path))}")
            
        return params

    def list_missions(self) -> List[Arma3Mission]:
        """List all available missions"""
        missions = []
        for item in self.missions_dir.glob("*"):
            if item.is_file() and item.suffix.lower() in ['.pbo', '.zip']:
                missions.append(Arma3Mission.from_path(item))
            elif item.is_dir():
                missions.append(Arma3Mission.from_path(item))
        return missions
    
    def install_mission(self, mission_path: Path) -> Arma3Mission:
        """Install a mission file or directory"""
        if not mission_path.exists():
            raise FileNotFoundError(f"Mission not found: {mission_path}")
        
        target_path = self.missions_dir / mission_path.name
        
        if mission_path.is_file():
            if mission_path.suffix.lower() == '.zip':
                # Extract ZIP archive
                with zipfile.ZipFile(mission_path, 'r') as zip_ref:
                    zip_ref.extractall(self.missions_dir)
                console.print(f"[green]Extracted mission from {mission_path.name}[/]")
            else:
                # Copy PBO or other files directly
                shutil.copy2(mission_path, target_path)
                console.print(f"[green]Installed mission: {mission_path.name}[/]")
        else:
            # Copy directory
            shutil.copytree(mission_path, target_path, dirs_exist_ok=True)
            console.print(f"[green]Installed mission directory: {mission_path.name}[/]")
            
        mission = Arma3Mission.from_path(target_path)
        if not self.active_mission:
            self.set_active_mission(mission)
        return mission
    
    def remove_mission(self, mission_name: str):
        """Remove a mission"""
        mission_path = self.missions_dir / mission_name
        if mission_path.exists():
            if mission_path.is_file():
                mission_path.unlink()
            else:
                shutil.rmtree(mission_path)
            console.print(f"[yellow]Removed mission: {mission_name}[/]")
            
            if self.active_mission and self.active_mission.path == mission_path:
                self.active_mission = None
        else:
            console.print(f"[red]Mission not found: {mission_name}[/]")
            
    def set_active_mission(self, mission: Arma3Mission):
        """Set the active mission for the server"""
        self.active_mission = mission
        console.print(f"[green]Set active mission to: {mission.name}[/]")
        self.save_config()

    def install(self):
        """Install Arma 3 server"""
        console.print("[yellow]Installing Arma 3 server...[/]")
        
        # Install server through SteamCMD
        self.steamcmd.install_app(self.ARMA3_APP_ID, Path(self.path))
        
        # Install workshop mods
        mods_dir = Path(self.path) / "mods"
        mods_dir.mkdir(parents=True, exist_ok=True)
        
        for mod in self.mods + self.server_mods:
            if mod.workshop_id:
                console.print(f"[yellow]Installing mod: {mod.name}[/]")
                self.steamcmd.install_workshop_item(
                    self.ARMA3_APP_ID,
                    mod.workshop_id,
                    mods_dir / mod.path
                )
        
        self.generate_config()
        console.print("[green]Server installation complete![/]")
        
    def start(self):
        """Start Arma 3 server"""
        # Create backup if enabled
        if self.backup_manager.backup_on_start:
            self.backup_manager.create_backup("before_start")
            
        # Start the server
        params = self.get_launch_parameters()
        console.print(f"[green]Starting {self.name} with parameters:[/]")
        console.print(" ".join(params))
        
        process = subprocess.Popen(
            [str(Path(self.path) / self.executable)] + params,
            cwd=self.path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Start monitoring
        self.monitor = ServerMonitor(process, Path(self.path) / "logs")
        self.monitor.add_restart_callback(self.restart)
        self.monitor.start_monitoring()
        
    def stop(self):
        """Stop Arma 3 server"""
        # Create backup if enabled
        if self.backup_manager.backup_on_stop:
            self.backup_manager.create_backup("before_stop")
            
        # Stop monitoring
        if self.monitor:
            self.monitor.stop_monitoring()
            self.monitor = None
            
        super().stop()
        
    def restart(self):
        """Restart the server"""
        console.print("[yellow]Restarting server...[/]")
        self.stop()
        self.start()
        
    def update(self):
        """Update server and mods"""
        console.print("[yellow]Checking for updates...[/]")
        
        # Update server
        self.steamcmd.install_app(self.ARMA3_APP_ID, Path(self.path), validate=True)
        
        # Update workshop mods
        mods_dir = Path(self.path) / "mods"
        for mod in self.mods + self.server_mods:
            if mod.workshop_id:
                console.print(f"[yellow]Updating mod: {mod.name}[/]")
                self.steamcmd.install_workshop_item(
                    self.ARMA3_APP_ID,
                    mod.workshop_id,
                    mods_dir / mod.path
                )
                
        console.print("[green]Updates complete![/]")
        
    def save_config(self):
        """Save server configuration to JSON"""
        config = {
            "name": self.server_name,
            "port": self.port,
            "max_players": self.max_players,
            "password": self.password,
            "admin_password": self.admin_password,
            "battle_eye": self.battle_eye,
            "mods": [{"name": mod.name, "path": mod.path, "workshop_id": mod.workshop_id} 
                    for mod in self.mods],
            "server_mods": [{"name": mod.name, "path": mod.path, "workshop_id": mod.workshop_id} 
                           for mod in self.server_mods],
            "active_mission": self.active_mission.name if self.active_mission else None
        }
        
        with open(self.config_dir / "cligsm_config.json", 'w') as f:
            json.dump(config, f, indent=2)
            
    def load_config(self):
        """Load server configuration from JSON"""
        config_file = self.config_dir / "cligsm_config.json"
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
                self.server_name = config["name"]
                self.port = config["port"]
                self.max_players = config["max_players"]
                self.password = config["password"]
                self.admin_password = config["admin_password"]
                self.battle_eye = config["battle_eye"]
                
                self.mods = [Arma3Mod(**mod) for mod in config["mods"]]
                self.server_mods = [Arma3Mod(**mod) for mod in config["server_mods"]]
                
                if config["active_mission"]:
                    mission_path = self.missions_dir / config["active_mission"]
                    if mission_path.exists():
                        self.active_mission = Arma3Mission.from_path(mission_path) 