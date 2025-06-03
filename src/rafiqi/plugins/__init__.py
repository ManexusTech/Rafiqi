"""Plugin system for Rafiqi"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class RafiqiPlugin(ABC):
    """Base class for all Rafiqi plugins"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the plugin"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what the plugin does"""
        pass
    
    @property
    @abstractmethod
    def commands(self) -> List[str]:
        """List of commands this plugin can handle"""
        pass
    
    @abstractmethod
    async def handle_command(self, command: str, args: Dict[str, Any]) -> str:
        """Handle a command with given arguments"""
        pass 