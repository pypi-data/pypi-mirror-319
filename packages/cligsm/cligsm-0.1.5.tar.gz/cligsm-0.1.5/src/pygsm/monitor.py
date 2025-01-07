"""
Server Performance Monitor and Auto-restart Manager
"""
import time
import psutil
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Callable
from rich.console import Console
from rich.live import Live
from rich.table import Table

console = Console()

class ServerMonitor:
    def __init__(self, process: psutil.Process, log_dir: Path):
        self.process = process
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.stats: List[Dict] = []
        self.restart_callbacks: List[Callable] = []
        
        # Monitoring thresholds
        self.cpu_threshold = 90  # CPU usage percentage
        self.memory_threshold = 90  # Memory usage percentage
        self.check_interval = 5  # Seconds between checks
        
    def start_monitoring(self):
        """Start monitoring the server"""
        if self.monitoring:
            return
            
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
    def stop_monitoring(self):
        """Stop monitoring the server"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
            
    def add_restart_callback(self, callback: Callable):
        """Add a callback to be called when server needs restart"""
        self.restart_callbacks.append(callback)
        
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                stats = self._collect_stats()
                self.stats.append(stats)
                
                # Keep last hour of stats
                if len(self.stats) > 3600 / self.check_interval:
                    self.stats.pop(0)
                
                self._check_thresholds(stats)
                self._log_stats(stats)
                
                time.sleep(self.check_interval)
                
            except psutil.NoSuchProcess:
                console.print("[red]Server process no longer exists![/]")
                self.monitoring = False
                break
                
    def _collect_stats(self) -> Dict:
        """Collect current server statistics"""
        cpu_percent = self.process.cpu_percent()
        memory = self.process.memory_info()
        memory_percent = self.process.memory_percent()
        
        return {
            "timestamp": datetime.now(),
            "cpu_percent": cpu_percent,
            "memory_used": memory.rss,
            "memory_percent": memory_percent,
            "threads": len(self.process.threads()),
            "handles": self.process.num_handles() if hasattr(self.process, 'num_handles') else 0
        }
        
    def _check_thresholds(self, stats: Dict):
        """Check if any thresholds are exceeded"""
        if stats["cpu_percent"] > self.cpu_threshold:
            console.print(f"[yellow]Warning: High CPU usage ({stats['cpu_percent']}%)[/]")
            self._trigger_restart()
            
        if stats["memory_percent"] > self.memory_threshold:
            console.print(f"[yellow]Warning: High memory usage ({stats['memory_percent']}%)[/]")
            self._trigger_restart()
            
    def _trigger_restart(self):
        """Trigger server restart"""
        for callback in self.restart_callbacks:
            try:
                callback()
            except Exception as e:
                console.print(f"[red]Error in restart callback: {e}[/]")
                
    def _log_stats(self, stats: Dict):
        """Log statistics to file"""
        log_file = self.log_dir / f"monitor_{stats['timestamp'].strftime('%Y%m%d')}.log"
        
        with open(log_file, 'a') as f:
            f.write(f"{stats['timestamp'].isoformat()},{stats['cpu_percent']},{stats['memory_percent']}\n")
            
    def get_current_stats(self) -> Table:
        """Get current statistics as a rich table"""
        table = Table(title="Server Performance")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        if self.stats:
            latest = self.stats[-1]
            table.add_row("CPU Usage", f"{latest['cpu_percent']}%")
            table.add_row("Memory Usage", f"{latest['memory_percent']}%")
            table.add_row("Memory (MB)", f"{latest['memory_used'] / 1024 / 1024:.1f}")
            table.add_row("Threads", str(latest['threads']))
            table.add_row("Handles", str(latest['handles']))
            
        return table
        
    def show_live_stats(self):
        """Show live statistics"""
        with Live(self.get_current_stats(), refresh_per_second=1) as live:
            while self.monitoring:
                live.update(self.get_current_stats())
                time.sleep(1) 