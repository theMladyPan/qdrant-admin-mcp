import logfire


def greet(name: str) -> str:
    """Greet a person by name
    
    Args:
        name: The name of the person to greet
    
    Returns:
        A greeting message
    """
    logfire.info("Greeting {name}", name=name)
    return f"Hello, {name}! Welcome to Qdrant Admin MCP."
