from fastapi import APIRouter, Query
from utils.amazon_hmac import buscar_produtos_amazon
from typing import Optional

router = APIRouter()

@router.get("/buscar")
async def buscar_amazon(termo: str = Query(..., min_length=2)):
    try:
        produtos = buscar_produtos_amazon(termo)
        return {"produtos": produtos}
    except Exception as e:
        return {"erro": str(e)}
