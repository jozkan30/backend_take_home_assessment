from fastapi import FastAPI
from .route import router as stock_router

app = FastAPI()

app.include_router(stock_router)