# Simple MCP Resource Provider

A minimal MCP server demonstrating static and parameterized resources, using
the FastMCP inspector for testing.

## Folder structure

```
mcp-resource-provider/
├── resource_demo.py      # the MCP server (3 resources)
├── documents/             # sample document files served by docs://{doc_id}
│   ├── 1.txt
│   ├── 2.txt
│   └── 3.txt
├── requirements.txt
└── README.md
```

## What's in `resource_demo.py`

- **`docs://list`** — static resource, returns the list of document IDs/titles
- **`docs://{doc_id}`** — parameterized resource, reads and returns the
  content of `documents/{doc_id}.txt`
- **`mcp://inspector`** — discovery resource, describes the server and its
  available resources

## Setup

```powershell
cd mcp-resource-provider
python -m venv .venv
.venv\Scripts\activate          # on macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` installs both:
- `mcp[cli]` — the official MCP Python SDK
- `fastmcp` — the standalone package that provides the `fastmcp` CLI command
  used to launch the Inspector

## Run the server directly

```powershell
python resource_demo.py
```

This just starts the server and waits for a client over stdio — nothing else
happens here, and that's expected.

## Inspect it with the FastMCP Inspector

```powershell
fastmcp dev inspector resource_demo.py
```

This opens a local URL in your browser. Click **Connect**, then go to the
**Resources** tab and try:

- `docs://list`
- `docs://1`, `docs://2`, `docs://3` (fill in the `doc_id` template field)
- `mcp://inspector`

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'mcp'`
Your venv doesn't have the package installed yet. With `(.venv)` active:
```powershell
pip install "mcp[cli]"
```
Verify with `pip show mcp`, and confirm you're actually inside the venv with
`python -c "import sys; print(sys.executable)"` — the path should point
inside `.venv\Scripts\`.

### `fastmcp : The term 'fastmcp' is not recognized...`
`mcp[cli]` only gives you the `mcp` command, not `fastmcp`. Install the
separate package:
```powershell
pip install fastmcp
```

### `Unknown command "resource_demo.py". Available commands: inspector, apps.`
You're on FastMCP 3.x, where `dev` became a command group. Use:
```powershell
fastmcp dev inspector resource_demo.py
```
(not `fastmcp dev resource_demo.py`)

### `File not found: ...\server.py`
Check the filename in your command matches the actual file — this project's
server file is `resource_demo.py`, not `server.py`.

### `Proxy Server PORT IS IN USE at port 6277`
An earlier Inspector session is still running in the background.
- Close any other terminal windows running `fastmcp dev`, or
- Free the port manually:
  ```powershell
  netstat -ano | findstr :6277
  taskkill /PID <pid_from_above> /F
  ```
- Or just use a different port:
  ```powershell
  fastmcp dev inspector resource_demo.py --port 6278
  ```

### Connection times out (`MCP error -32001: Request timed out`)
STDIO transport reserves **stdout** entirely for JSON-RPC protocol messages.
Any stray `print()` to stdout corrupts the stream and the Inspector hangs
waiting for a valid reply. Always send human-readable logging to **stderr**:
```python
print("Starting server", file=sys.stderr)
```
This project's `resource_demo.py` already does this correctly.

### `IndentationError: unindent does not match any outer indentation level`
Usually caused by mixed tabs/spaces from copy-pasting between editors. Fix by
re-pasting the whole file cleanly, or in VS Code check the indentation
indicator in the bottom status bar for a tabs/spaces mismatch warning.

### `Invalid JSON: EOF while parsing a value ... input_value='\n'`
This is a known, currently open bug in the official MCP Python SDK's stdio
transport, most commonly reported on **Windows** — a stray blank line gets
sent over the pipe and the client fails to parse it as JSON. It is not
caused by anything in this project's code.

Two workarounds, in order of effort:
1. **Update packages** — sometimes already patched:
   ```powershell
   pip install --upgrade "mcp[cli]" fastmcp
   ```
2. **Run from WSL instead of native Windows** (most reliable fix, since the
   bug is tied to Windows-specific pipe/line-ending handling):
   ```powershell
   wsl --install
   ```
   Then inside the WSL/Ubuntu terminal:
   ```bash
   cd /mnt/d/Desktop/Claude/MCP/DEMO_2/mcp-resource-provider
   python3 -m venv .venv
   source .venv/bin/activate
   pip install "mcp[cli]" fastmcp
   fastmcp dev inspector resource_demo.py
   ```
