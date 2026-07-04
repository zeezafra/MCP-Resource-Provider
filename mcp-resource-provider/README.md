# Simple MCP Resource Provider

A minimal MCP server demonstrating static and parameterized resources.

## Folder structure

```
mcp-resource-provider/
├── resource_demo.py     # the MCP server (3 resources)
├── documents/            # sample document files served by docs://{doc_id}
│   ├── 1.txt
│   ├── 2.txt
│   └── 3.txt
├── requirements.txt
└── README.md
```

## Setup

```bash
cd mcp-resource-provider
python -m venv .venv
source .venv/bin/activate      # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the server

```bash
python resource_demo.py
```

This just starts the server and waits for a client — nothing else happens here.

## Inspect it

In a **second terminal** (same folder, same venv activated):

```bash
fastmcp dev resource_demo.py
```

This opens the FastMCP Inspector UI. Go to the **Resources** tab and try:

- `docs://list` — returns the list of documents
- `docs://1`, `docs://2`, `docs://3` — returns the content of each document (read from the `documents/` folder)
- `mcp://inspector` — describes the server and its resources
