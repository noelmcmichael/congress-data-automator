"""
Simple test API to verify GET endpoints work with production database
"""
import os
import sys
sys.path.insert(0, 'backend')
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Test Congressional Data API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the data retrieval router
from app.api.v1.data_retrieval import router as data_retrieval_router
app.include_router(data_retrieval_router, prefix="/api/v1", tags=["data-retrieval"])

@app.get("/")
async def root():
    return {"message": "Test Congressional Data API", "status": "active"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)