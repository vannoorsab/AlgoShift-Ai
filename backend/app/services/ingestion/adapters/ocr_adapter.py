from abc import ABC, abstractmethod
from typing import Dict, Any

class OCRAdapter(ABC):
    @abstractmethod
    async def extract_ocr(self, file_path: str, **kwargs) -> str:
        """Sample video frames and extract on-screen OCR text."""
        pass

class MockTesseractOCRAdapter(OCRAdapter):
    async def extract_ocr(self, file_path: str, **kwargs) -> str:
        filename = file_path.split("/")[-1].split("\\")[-1]
        return f"OCR Text detected from frames ({filename}): JAVA DEVELOPER 2 AM"
