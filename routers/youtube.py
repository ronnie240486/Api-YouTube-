
from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/buscar")
def buscar_videos(termo: str = Query(..., min_length=2)):
    return [
        {
            "canal": "Canal Exemplo",
            "titulo": f"Vídeo sobre {termo}",
            "views": "1.234.567",
            "cpm": "R$ 12,34",
            "receita": "R$ 15.000",
            "duracao": "8:35",
            "publicado": "3 dias atrás",
            "hashtags": ["#exemplo", f"#{termo}"],
            "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
            "link": "https://youtube.com/watch?v=dQw4w9WgXcQ"
        }
    ]
