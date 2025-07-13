from fastapi import APIRouter

router = APIRouter()

@router.get("/buscar")
def buscar_produtos(termo: str):
    return {"erro": "Amazon API real em construção (autenticação HMAC necessária)"}
