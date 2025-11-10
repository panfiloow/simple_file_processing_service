from fastapi import FastAPI
from app.core.config import settings

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Simple File Processing Service", "version": settings.VERSION}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}