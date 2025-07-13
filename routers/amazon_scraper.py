from fastapi import APIRouter
from utils.amazon_api import buscar_produtos_reais

router = APIRouter()

@router.get("/amazon/buscar")
def buscar_produtos(termo: str):
    return buscar_produtos_reais(termo)
