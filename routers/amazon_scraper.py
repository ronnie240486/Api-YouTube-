import os
import logging
from fastapi import APIRouter, Query
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Configurar logger
logger = logging.getLogger("amazon_debug")
handler = logging.FileHandler("amazon_debug.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

@router.get("/buscar")
def buscar_amazon(termo: str = Query(..., min_length=2)):
    access_key = os.getenv("AMAZON_ACCESS_KEY")
    secret_key = os.getenv("AMAZON_SECRET_KEY")
    tag = os.getenv("AMAZON_TAG")
    region = os.getenv("AMAZON_REGION", "us-east-1")

    if not all([access_key, secret_key, tag]):
        logger.error("Credenciais da Amazon não definidas")
        return {"erro": "Credenciais da Amazon não estão definidas no .env"}

    # Simulação de chamada (para evitar erro de build no Render)
    fake_response = [
        {"titulo": "Produto 1", "preco": "R$ 199,90", "imagem": "https://via.placeholder.com/100"},
        {"titulo": "Produto 2", "preco": "R$ 299,90", "imagem": "https://via.placeholder.com/100"},
        {"titulo": "Produto 3", "preco": "R$ 399,90", "imagem": "https://via.placeholder.com/100"},
    ]
    logger.info(f"Busca Amazon por: {termo}")
    return fake_response