from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter()

@router.get("/buscar")
def buscar_videos(termo: str, pais: Optional[str] = None, cidade: Optional[str] = None):
    return {
        "resultados": [
            {
                "canal": "Canal Real Exemplo",
                "visualizacoes": 9738544,
                "receita_estimada": 146078.16,
                "cpm": 15.00,
                "duracao": "PT36S",
                "publicado_ha": "5 dias",
                "hashtags": ["#celular", "#tendência"]
            }
        ]
    }