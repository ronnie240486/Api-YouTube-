from fastapi import APIRouter
import os
from dotenv import load_dotenv
import logging

load_dotenv()

router = APIRouter()

@router.get("/amazon/teste-variaveis")
def testar_variaveis():
    access_key = os.getenv("AMAZON_ACCESS_KEY")
    secret_key = os.getenv("AMAZON_SECRET_KEY")
    tag = os.getenv("AMAZON_TAG")
    region = os.getenv("AMAZON_REGION")

    if not all([access_key, secret_key, tag, region]):
        return {
            "erro": "Alguma variável de ambiente não foi definida",
            "AMAZON_ACCESS_KEY": bool(access_key),
            "AMAZON_SECRET_KEY": bool(secret_key),
            "AMAZON_TAG": bool(tag),
            "AMAZON_REGION": bool(region)
        }

    return {
        "mensagem": "✅ Todas as variáveis de ambiente foram carregadas corretamente!",
        "AMAZON_TAG": tag,
        "AMAZON_REGION": region
    }
