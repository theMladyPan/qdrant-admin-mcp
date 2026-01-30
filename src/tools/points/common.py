from fastembed import TextEmbedding

_embedding_models: dict[str, TextEmbedding] = {}


def get_embedding_model(model_name: str = "BAAI/bge-small-en-v1.5") -> TextEmbedding:
    """Get or create cached instance of embedding model

    Args:
        model_name: Name of the fastembed model to use

    Returns:
        TextEmbedding instance
    """
    global _embedding_models
    if model_name not in _embedding_models:
        _embedding_models[model_name] = TextEmbedding(model_name=model_name)
    return _embedding_models[model_name]
