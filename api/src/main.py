# main.py
from fastapi import FastAPI
from routes import router as api_router

def create_application() -> FastAPI:
    app = FastAPI(title='Audio Response System', version='1.0.0')
    app.include_router(api_router)
    return app

app = create_application()
