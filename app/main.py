from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.views.routes import view_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(view_router, prefix="",)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

