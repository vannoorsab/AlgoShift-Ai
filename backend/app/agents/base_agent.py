from abc import ABC, abstractmethod
from typing import Any, Dict
from app.models.enums import AgentStatus

class BaseAgent(ABC):
    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name

    @abstractmethod
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent task asynchronously."""
        pass
