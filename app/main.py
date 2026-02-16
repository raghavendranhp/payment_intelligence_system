from fastapi import FastAPI
from app.routers import payment_routes


app = FastAPI(
    title="SeShat AI Payment Intelligence System",
    description="AI-driven payment analysis and fraud detection API",
    version="1.0.0"
)


app.include_router(payment_routes.router)


async def root():
    return {
        "message": "Welcome to the SeShat AI Payment Intelligence API.",
        "status": "Running",
        "docs_url": "/docs"  
    }