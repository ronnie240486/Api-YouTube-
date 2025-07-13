from fastapi import APIRouter, Query
from pydantic import BaseModel
import datetime

router = APIRouter()

class Video(BaseModel):
    titulo: str
    visualizacoes: int
    receita_estimada: float
    duracao: str
    tempo: str
    link: str

@router.get("/buscar")
def buscar_videos(termo: str = Query(...)):
    # Simulado com dados estáticos
    return {"videos": [
        {
            "titulo": f"Vídeo sobre {termo}",
            "visualizacoes": 1234567,
            "receita_estimada": 321.99,
            "duracao": "PT3M12S",
            "tempo": "há 2 dias",
            "link": "https://youtube.com"
        }
    ]}
