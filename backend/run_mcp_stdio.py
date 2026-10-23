"""
TransplantLink MCP Stdio Runner
Allows running the TransplantLink MCP server directly over standard input/output (stdio)
for integrations with Claude Desktop, Antigravity, and ChatGPT MCP connectors.
"""

import sys
from pathlib import Path

# Add project root to python path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.mcp_server import mcp_server

if __name__ == "__main__":
    print("Starting TransplantLink MCP Server (stdio transport)...", file=sys.stderr)
    mcp_server.run()
