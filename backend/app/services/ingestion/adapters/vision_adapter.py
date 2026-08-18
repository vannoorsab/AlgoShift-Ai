from abc import ABC, abstractmethod
from typing import Dict, Any

class VisualAnalysisAdapter(ABC):
    @abstractmethod
    async def describe_visuals(self, file_path: str, **kwargs) -> str:
        """Sample video frames and generate visual scene description."""
        pass

class MockVisionAdapter(VisualAnalysisAdapter):
    async def describe_visuals(self, file_path: str, **kwargs) -> str:
        filename = file_path.split("/")[-1].split("\\")[-1]
        return f"Visual Description ({filename}): Software developer seated at desk editing code on modern IDE display."
