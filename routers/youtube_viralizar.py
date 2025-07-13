from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter()

@router.get("/buscar")
async def buscar_youtube(termo: str = Query(...), pais: Optional[str] = "br"):
    return {"videos": [{
        "titulo": f"Vídeo sobre {termo}",
        "canal": "Canal Exemplo",
        "views": "1.234.567",
        "receita": "R$ 15.340,50",
        "thumbnail": "https://i.ytimg.com/vi/abcd1234hqdefault.jpg",
        "link": "https://youtube.com/watch?v=abcd1234"
    }]}
