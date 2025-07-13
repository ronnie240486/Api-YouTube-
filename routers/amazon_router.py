
from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/testar")
def testar_variaveis():
    keys = {
        "AWS_ACCESS_KEY": os.getenv("AWS_ACCESS_KEY"),
        "AWS_SECRET_KEY": os.getenv("AWS_SECRET_KEY"),
        "AMAZON_TAG": os.getenv("AMAZON_TAG"),
        "REGION": os.getenv("REGION"),
        "ENDPOINT": os.getenv("ENDPOINT")
    }

    faltando = [k for k, v in keys.items() if not v]
    if faltando:
        return {"erro": f"Variáveis faltando: {', '.join(faltando)}"}

    return {"ok": "Todas as variáveis carregadas com sucesso", "variaveis": keys}
