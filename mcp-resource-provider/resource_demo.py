import sys

from mcp.server.fastmcp import FastMCP
from pathlib import Path

mcp = FastMCP(name="simple-resource-demo")

DOCS_DIR = Path(__file__).parent / "documents"

DOC_TITLES = {
    "1": "Introduction",
    "2": "Setup Guide",
    "3": "Notes",
}


# 1) Resource: list documents
@mcp.resource("docs://list")
def list_docs():
    return [{"id": doc_id, "title": title} for doc_id, title in DOC_TITLES.items()]


# 2) Resource: fetch a single document
@mcp.resource("docs://{doc_id}")
def get_doc(doc_id: str):
    file_path = DOCS_DIR / f"{doc_id}.txt"
    if not file_path.exists():
        return {"id": doc_id, "error": f"No document found for id '{doc_id}'."}

    return {
        "id": doc_id,
        "title": DOC_TITLES.get(doc_id, "Untitled"),
        "content": file_path.read_text().strip(),
    }


# 3) Resource: inspector (shows available resources)
@mcp.resource("mcp://inspector")
def inspector():
    return {
        "server": mcp.name,
        "resources": [
            "docs://list",
            "docs://{doc_id}",
            "mcp://inspector",
        ],
    }


if __name__ == "__main__":
    print("Starting Simple MCP Resource Demo", file=sys.stderr)
    mcp.run()