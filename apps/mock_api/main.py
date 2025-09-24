from fastapi import FastAPI
from .router import router

app = FastAPI(title="Mock Shop API")
app.include_router(router)
