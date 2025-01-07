"""
Configuration management for PyGSM
"""
import os
import json
from pathlib import Path
from typing import Dict, Any

CONFIG_DIR = Path.home() / ".pygsm"
CONFIG_FILE = CONFIG_DIR / "config.json"

def ensure_config_dir():
    """Ensure the configuration directory exists"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def load_config() -> Dict[str, Any]:
    """Load the configuration file"""
    ensure_config_dir()
    if not CONFIG_FILE.exists():
        return {}
    
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config: Dict[str, Any]):
    """Save the configuration file"""
    ensure_config_dir()
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def get_server_path(game: str) -> Path:
    """Get the installation path for a game server"""
    config = load_config()
    return Path(config.get('server_paths', {}).get(game, str(CONFIG_DIR / 'servers' / game))) 