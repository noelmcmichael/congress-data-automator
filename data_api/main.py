"""
Separate data retrieval API service for Congressional Data
"""
import os
import sys
from pathlib import Path

# Add the backend directory to the path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.data_retrieval import router as data_retrieval_router

app = FastAPI(
    title="Congressional Data API",
    description="Data retrieval endpoints for Congressional Data Automation Service",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the data retrieval router
app.include_router(data_retrieval_router, prefix="/api/v1", tags=["data-retrieval"])

@app.get("/")
async def root():
    return {
        "message": "Congressional Data API",
        "status": "active",
        "version": "1.0.0",
        "endpoints": {
            "members": "/api/v1/members",
            "committees": "/api/v1/committees", 
            "hearings": "/api/v1/hearings"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)