
from fastapi import APIRouter, Query
from utils.amazon_api_hmac import buscar_produtos_amazon

router = APIRouter()

@router.get("/buscar")
def buscar(termo: str = Query(..., min_length=2)):
    try:
        return buscar_produtos_amazon(termo)
    except Exception as e:
        return {"erro": str(e)}
