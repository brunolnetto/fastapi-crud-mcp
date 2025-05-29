# server/main.py
from copy import deepcopy

from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

from backend.server.models import Base
from backend.server.db import engine
from backend.server.routes import router

# Create all tables
Base.metadata.create_all(bind=engine)

# Tag descriptions (optional, but good for docs)
tags_metadata = [
    {
        "name": "items",
        "description": "Operations related to item management—create, read, update, delete."
    }
]

# Initialize FastAPI app
app = FastAPI(
    title="My MCP API",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=tags_metadata,
)

# Include your regular CRUD router
app.include_router(router, prefix="/api", tags=["Items"])

# === FastAPI-MCP wiring ===
mcp = FastApiMCP(
    app,
    name="My API MCP",                      # human-friendly name
    description="MCP server for Item CRUD",  
    describe_all_responses=True,            # Include all possible response schemas
    describe_full_response_schema=True,     # Include full JSON schema in descriptions
    include_tags=["items"]
)

# Mount into the same ASGI app
mcp.mount()

# Refresh the MCP server
mcp.setup_server()

# Run the app
if __name__ == "__main__": # pragma: no cover
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)