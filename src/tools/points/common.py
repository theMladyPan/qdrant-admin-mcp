from fastembed import TextEmbedding

_embedding_model = None

def get_embedding_model(model_name: str = "BAAI/bge-small-en-v1.5") -> TextEmbedding:
    """Get or create singleton instance of embedding model"""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = TextEmbedding(model_name=model_name)
    return _embedding_model
