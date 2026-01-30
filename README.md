# Qdrant Admin MCP

![Python](https://img.shields.io/badge/python-3.13+-blue.svg?logo=python&logoColor=white)
![FastMCP](https://img.shields.io/badge/FastMCP-2.14.4-orange.svg)
![Version](https://img.shields.io/badge/version-1.0.0-purple.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg?logo=docker&logoColor=white)](Dockerfile)
[![Deployment](https://img.shields.io/badge/deploy-europe--west1-4285F4.svg?logo=google-cloud&logoColor=white)](https://console.cloud.google.com/run/detail/europe-west1/qdrant-admin-mcp/metrics?project=mcp-servers-485920)

A Model Context Protocol (MCP) server for managing Qdrant vector databases. 
Built with [FastMCP](https://github.com/fastmcp/fastmcp) and `qdrant-client`'s async API.

## Features

*   **Collection Management**: Create, delete, list, and inspect collections.
*   **Snapshot Management**: Backup and restore collections via snapshots.
*   **Data Operations**: Search, retrieve, upsert, and delete points.
*   **Async Performance**: Built on `AsyncQdrantClient` for non-blocking operations.
*   **Multi-Tenancy**: Supports connecting to different Qdrant instances via request headers.

## Public Deployment

This MCP server is publicly available at:

```
https://qdrant-admin-mcp.rubint.sk/sse
```

It is a stateless service that connects to the Qdrant instance specified in your request headers. Your API keys are never stored on the server.

## Configuration

To use this server with your MCP client (e.g., Claude Desktop, Cursor), add it to your configuration.

### Example Configuration (`claude_desktop_config.json`)

- Replace `YOUR_QDRANT_URL` and `YOUR_QDRANT_API_KEY` with your actual credentials. 
- Select the appropriate tools as needed (e.g. omit tools you don't want to use) like deleting collections or snapshots.)

```json
{
  "mcpServers": {
    "qdrant-admin": {
      "type": "sse",
      "url": "https://qdrant-admin-mcp.rubint.sk/sse",
      "tools": ["*"],
      "headers": {
        "X-Qdrant-Url": "https://xyz-example.eu-central.aws.cloud.qdrant.io:6333",
        "X-Qdrant-Api-Key": "your-qdrant-api-key-here"
      }
    }
  }
}
```

### Local Development

If you prefer to run the server locally:

1.  **Install dependencies:**
    ```bash
    uv sync
    ```

2.  **Run the server:**
    ```bash
    uv run python main.py
    ```

3.  **Docker:**
    ```bash
    docker build -t qdrant-admin-mcp .
    docker run -p 8080:8080 qdrant-admin-mcp
    ```

## Contributing

We welcome contributions! Please check `AGENTS.md` for developer documentation, architectural decisions, and source code navigation.

## License

MIT
