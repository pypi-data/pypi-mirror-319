"""
Backup Manager for server files and configurations
"""
import shutil
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import zipfile
from rich.console import Console
from rich.progress import track

console = Console()

class BackupManager:
    def __init__(self, server_path: Path, backup_dir: Path):
        self.server_path = server_path
        self.backup_dir = backup_dir
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Default backup settings
        self.max_backups = 5
        self.backup_on_start = True
        self.backup_on_stop = True
        self.include_mods = False
        
    def create_backup(self, name: str = None) -> Path:
        """Create a new backup"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = name or f"backup_{timestamp}"
        backup_path = self.backup_dir / backup_name
        
        console.print(f"[yellow]Creating backup: {backup_name}[/]")
        
        # Create backup directory
        backup_path.mkdir(parents=True, exist_ok=True)
        
        # Save metadata
        metadata = {
            "timestamp": timestamp,
            "name": backup_name,
            "server_name": self.server_path.name,
            "include_mods": self.include_mods
        }
        
        with open(backup_path / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Backup configuration files
        self._backup_configs(backup_path)
        
        # Backup missions
        self._backup_missions(backup_path)
        
        # Backup mods if enabled
        if self.include_mods:
            self._backup_mods(backup_path)
            
        # Compress backup
        shutil.make_archive(str(backup_path), 'zip', backup_path)
        shutil.rmtree(backup_path)
        
        console.print(f"[green]Backup created: {backup_name}.zip[/]")
        
        # Clean up old backups
        self._cleanup_old_backups()
        
        return backup_path.with_suffix('.zip')
    
    def restore_backup(self, backup_path: Path):
        """Restore from a backup"""
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup not found: {backup_path}")
            
        console.print(f"[yellow]Restoring from backup: {backup_path.stem}[/]")
        
        # Create temporary directory for extraction
        temp_dir = self.backup_dir / "temp_restore"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Extract backup
            shutil.unpack_archive(backup_path, temp_dir)
            
            # Read metadata
            with open(temp_dir / "metadata.json") as f:
                metadata = json.load(f)
            
            # Restore configurations
            if (temp_dir / "config").exists():
                self._restore_directory(temp_dir / "config", self.server_path / "config")
                
            # Restore missions
            if (temp_dir / "missions").exists():
                self._restore_directory(temp_dir / "missions", self.server_path / "mpmissions")
                
            # Restore mods if they were included
            if metadata.get("include_mods") and (temp_dir / "mods").exists():
                self._restore_directory(temp_dir / "mods", self.server_path / "mods")
                
            console.print(f"[green]Backup restored successfully![/]")
            
        finally:
            # Clean up
            shutil.rmtree(temp_dir)
            
    def list_backups(self) -> List[Dict]:
        """List all available backups"""
        backups = []
        for backup_file in self.backup_dir.glob("*.zip"):
            try:
                with zipfile.ZipFile(backup_file) as zip_ref:
                    with zip_ref.open("metadata.json") as f:
                        metadata = json.load(f)
                        metadata["file_path"] = backup_file
                        metadata["size"] = backup_file.stat().st_size
                        backups.append(metadata)
            except Exception as e:
                console.print(f"[red]Error reading backup {backup_file.name}: {e}[/]")
                
        return sorted(backups, key=lambda x: x["timestamp"], reverse=True)
    
    def _backup_configs(self, backup_path: Path):
        """Backup configuration files"""
        config_backup = backup_path / "config"
        config_backup.mkdir(parents=True, exist_ok=True)
        
        config_dir = self.server_path / "config"
        if config_dir.exists():
            self._copy_with_progress(config_dir, config_backup, "Backing up configurations")
            
    def _backup_missions(self, backup_path: Path):
        """Backup mission files"""
        missions_backup = backup_path / "missions"
        missions_backup.mkdir(parents=True, exist_ok=True)
        
        missions_dir = self.server_path / "mpmissions"
        if missions_dir.exists():
            self._copy_with_progress(missions_dir, missions_backup, "Backing up missions")
            
    def _backup_mods(self, backup_path: Path):
        """Backup mod files"""
        mods_backup = backup_path / "mods"
        mods_backup.mkdir(parents=True, exist_ok=True)
        
        mods_dir = self.server_path / "mods"
        if mods_dir.exists():
            self._copy_with_progress(mods_dir, mods_backup, "Backing up mods")
            
    def _copy_with_progress(self, src: Path, dst: Path, description: str):
        """Copy files with progress bar"""
        files = list(src.rglob("*"))
        for file in track(files, description=description):
            if file.is_file():
                rel_path = file.relative_to(src)
                dst_path = dst / rel_path
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, dst_path)
                
    def _restore_directory(self, src: Path, dst: Path):
        """Restore a directory from backup"""
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        
    def _cleanup_old_backups(self):
        """Remove old backups exceeding max_backups"""
        backups = self.list_backups()
        if len(backups) > self.max_backups:
            for backup in backups[self.max_backups:]:
                backup_path = backup["file_path"]
                backup_path.unlink()
                console.print(f"[yellow]Removed old backup: {backup_path.name}[/]") 