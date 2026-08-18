from abc import ABC, abstractmethod
from typing import Dict, Any

class TranscriptionAdapter(ABC):
    @abstractmethod
    async def transcribe(self, file_path: str, **kwargs) -> str:
        """Extract audio and generate transcript text from video file."""
        pass

class MockWhisperTranscriptionAdapter(TranscriptionAdapter):
    async def transcribe(self, file_path: str, **kwargs) -> str:
        filename = file_path.split("/")[-1].split("\\")[-1]
        return f"Transcript extracted from uploaded video file ({filename}): Java backend microservices setup and production deployment."
