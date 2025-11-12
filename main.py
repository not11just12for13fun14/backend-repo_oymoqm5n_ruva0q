from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, Dict
import os
from database import db

app = FastAPI(title="The 16th Element API")

# CORS for local dev and preview
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root() -> Dict[str, Any]:
    return {"message": "Backend running", "service": "16th-element"}


@app.get("/test")
def test_db() -> Dict[str, Any]:
    database_url = os.getenv("DATABASE_URL")
    database_name = os.getenv("DATABASE_NAME")

    status = {
        "backend": "ok",
        "database": "configured" if db is not None else "not_configured",
        "database_url": f"{database_url[:6]}..." if database_url else None,
        "database_name": database_name,
        "connection_status": "connected" if db is not None else "disconnected",
        "collections": []
    }

    try:
        if db is not None:
            status["collections"] = db.list_collection_names()
    except Exception as e:
        status["connection_status"] = f"error: {e}"  # surface any connection issues

    return status


@app.get("/schema")
def get_schema() -> Dict[str, Any]:
    """Return schemas.py content so external tools can introspect collections."""
    try:
        with open("schemas.py", "r", encoding="utf-8") as f:
            content = f.read()
        return {"status": "ok", "content": content}
    except Exception as e:
        return {"status": "error", "error": str(e)}
