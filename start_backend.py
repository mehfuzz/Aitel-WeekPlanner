"""Backend startup wrapper that patches motor with mongomock-motor for in-memory MongoDB
and serves the built frontend static files."""
import sys
import os

# Patch motor.motor_asyncio to use mongomock_motor before any server imports
from mongomock_motor import AsyncMongoMockClient
import motor.motor_asyncio
motor.motor_asyncio.AsyncIOMotorClient = AsyncMongoMockClient

# Now import the server app
from backend.server import app
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Mount the built React frontend
FRONTEND_BUILD = os.path.join(os.path.dirname(__file__), "frontend", "build")

if os.path.exists(FRONTEND_BUILD):
    # Serve static assets
    app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND_BUILD, "static")), name="static")

    # Catch-all route to serve React app (must be last)
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        index = os.path.join(FRONTEND_BUILD, "index.html")
        return FileResponse(index)

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        reload=False,
    )
