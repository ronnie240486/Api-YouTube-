
from fastapi import APIRouter, Query
import random

router = APIRouter()

@router.get("/buscar")
def buscar_videos(termo: str = Query(...)):
    if termo.lower() == "vazio":
        return {"videos": []}  # simula nenhum resultado
    else:
        return {
            "videos": [
                {
                    "titulo": f"Vídeo sobre {termo}",
                    "canal": "Canal Exemplo",
                    "views": f"{random.randint(1000, 1000000)}",
                    "receita": "R$ {:.2f}".format(random.uniform(10, 300)),
                    "cpm": "R$ {:.2f}".format(random.uniform(5, 30)),
                    "duracao": "PT5M30S",
                    "publicado": "2 dias atrás",
                    "hashtags": ["#" + termo.lower(), "#tendência"]
                }
            ]
        }
