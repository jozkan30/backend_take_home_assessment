from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.security import APIKeyHeader
from .service import AlphaVantageAPI
import logging

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
router = APIRouter()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
api_key_header = APIKeyHeader(name="Authorization", auto_error=True)
limiter = Limiter(
    key_func=get_remote_address,
    strategy="fixed-window",
    storage_uri="memory://"
)

def get_api_key(api_key: str = Depends(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=401, detail="Please provide API Key")
    return api_key

def get_alpha_vantage_service(request: Request):
    return AlphaVantageAPI(request.headers.get("Authorization"))

@router.get("/sample", dependencies=[])
@limiter.limit("2/seconds")
def sample(request: Request, service:AlphaVantageAPI = Depends(get_alpha_vantage_service) ):
    return service.fetch_sample_data()

@router.get("/status", dependencies=[])
def status():
    return {"app": "Server is running!"}

@router.get("/lookup", dependencies=[Depends(get_api_key)])
@limiter.limit("10/minute")
def lookup(request: Request, symbol: str, date: str, service: AlphaVantageAPI = Depends(get_alpha_vantage_service)):
    return service.lookup(symbol, date)

@router.get("/min", dependencies=[Depends(get_api_key)])
@limiter.limit("10/minute")
def lookup(request: Request, symbol: str, days: int, service: AlphaVantageAPI = Depends(get_alpha_vantage_service)):
    return service.get_lowest_low(symbol, days)

@router.get("/max", dependencies=[Depends(get_api_key)])
@limiter.limit("10/minute")
def lookup(request: Request, symbol: str, days: int, service: AlphaVantageAPI = Depends(get_alpha_vantage_service)):
    return service.get_highest_high(symbol, days)