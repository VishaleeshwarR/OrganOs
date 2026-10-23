"""
TransplantLink Backend Launcher
Starts the FastAPI server with MCP bridge on port 8000.
"""

import uvicorn
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    print(f"Starting TransplantLink API & MCP Bridge on http://{host}:{port} ...")
    uvicorn.run("backend.server:app", host=host, port=port, reload=True)
