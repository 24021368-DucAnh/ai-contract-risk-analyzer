from fastapi import FastAPI

from app.api.routes.health import router as health_router

app = FastAPI(
    title="AI Contract Risk Analyzer API",
    version="0.1.0"
)

app.include_router(health_router)


@app.get("/")
def root():
    return {
        "message": "AI Contract Risk Analyzer API"
    }