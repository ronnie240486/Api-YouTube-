
from fastapi import APIRouter, Query
from utils.amazon_api import buscar_produtos_reais

router = APIRouter()

@router.get("/amazon/buscar")
def buscar_produtos(termo: str = Query(..., min_length=2)):
    try:
        return buscar_produtos_reais(termo)
    except Exception as e:
        return {"erro": str(e)}
