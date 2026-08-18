from typing import List

class VectorEmbeddingService:
    """Interface for generating text/transcript embeddings for MongoDB vector search."""
    
    async def generate_embedding(self, text: str) -> List[float]:
        # Placeholder returning dummy 1536-dim vector for testing
        return [0.0] * 1536
