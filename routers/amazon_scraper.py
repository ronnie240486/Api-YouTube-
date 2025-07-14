from fastapi import APIRouter
from utils.amazon_api import buscar_produtos_amazon

router = APIRouter()

@router.get("/amazon/buscar")
def buscar_amazon(termo: str):
    return buscar_produtos_amazon(termo)
