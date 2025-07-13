
from fastapi import APIRouter
import os
import requests

router = APIRouter(prefix="/amazon")

@router.get("/buscar")
def buscar_amazon(termo: str):
    access_key = os.getenv("AWS_ACCESS_KEY")
    secret_key = os.getenv("AWS_SECRET_KEY")
    tag = os.getenv("AMAZON_TAG")

    if not all([access_key, secret_key, tag]):
        return {"erro": "Credenciais da Amazon não estão definidas no .env"}

    # Simulação de retorno (substituir pela chamada PAAPI real com assinatura HMAC)
    return [
        {
            "titulo": f"{termo} - Produto Exemplo",
            "imagem": "https://via.placeholder.com/300x200.png?text=Produto",
            "preco": "R$ 129,99",
            "avaliacao": "4.5",
            "link": "https://www.amazon.com.br/"
        }
    ]
