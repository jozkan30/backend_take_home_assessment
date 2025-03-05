from fastapi import APIRouter, HTTPException, Request, Depends
from .service import AlphaVantageAPI
import logging

router = APIRouter()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def get_alpha_vantage_service(request: Request):
    api_key = request.headers.get("Authorization")
    if not api_key:
        raise HTTPException(status_code=401, detail="API key is required")
    return AlphaVantageAPI(api_key)

@router.get("/status")
def status():
    return {"app": "Server is running!"}

@router.get("/lookup")
def lookup(symbol: str, date: str, service: AlphaVantageAPI = Depends(get_alpha_vantage_service)):
    return service.lookup(symbol, date)

@router.get("/min")
def lookup(symbol: str, days: int, service: AlphaVantageAPI = Depends(get_alpha_vantage_service)):
    return service.get_lowest_low(symbol, days)

@router.get("/max")
def lookup(symbol: str, days: int, service: AlphaVantageAPI = Depends(get_alpha_vantage_service)):
    return service.get_highest_high(symbol, days)