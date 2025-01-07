"""
Server management functionality for PyGSM
"""
from dataclasses import dataclass
from typing import Optional
import os
import subprocess

@dataclass
class GameServer:
    name: str
    path: str
    executable: str
    config_file: Optional[str] = None
    process: Optional[subprocess.Popen] = None

    def install(self):
        """Install the game server"""
        # Implementation will vary by game type
        raise NotImplementedError(f"Installation for {self.name} not implemented yet")

    def start(self):
        """Start the game server"""
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Server directory not found: {self.path}")
        
        if self.process and self.process.poll() is None:
            raise RuntimeError("Server is already running")
        
        # Basic implementation - will need to be enhanced per game type
        self.process = subprocess.Popen(
            [self.executable],
            cwd=self.path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    def stop(self):
        """Stop the game server"""
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait(timeout=30)
        else:
            raise RuntimeError("Server is not running")

    def status(self) -> bool:
        """Check if the server is running"""
        return bool(self.process and self.process.poll() is None) 